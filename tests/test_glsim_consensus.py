"""GLSim contract smoke and simulator rollback checks.

The agreement smoke case captures and replays the contract's validator
callback in one local process. It is not evidence of independent validator
nodes. A separate synthetic test checks GLSim's snapshot rollback path.
"""

import copy
import hashlib
import json
import re
from types import SimpleNamespace

import glsim.consensus as sim_consensus
from glsim.engine import SimEngine
from glsim.state import StateStore
from glsim.tx_decoder import encode_result_bytes
from gltest.direct import loader


URLS = (
    "https://evidence-a.example/report.txt",
    "https://evidence-b.example/report.txt",
)
BODIES = (
    b"The signed release manifest states version 4.2 was published on 2026-10-10.",
    b"The official changelog lists version 4.2 with release date 2026-10-10.",
)


def _manifest():
    return json.dumps(
        [
            {"url": url, "sha256": hashlib.sha256(body).hexdigest()}
            for url, body in zip(URLS, BODIES, strict=True)
        ],
        separators=(",", ":"),
    )


def _run_consensus_case(monkeypatch):
    engine = SimEngine(StateStore(seed="consensusguard-glsim-tests"))
    engine.num_validators = 5
    engine.max_rotations = 3
    engine.activate()
    # Keep GLSim's process-local direct-mode integration isolated.
    monkeypatch.setattr(engine, "_ensure_direct_mode_runtime_patches", lambda: None)

    original_restore = sim_consensus._restore_storages

    def restore_storage_and_contract_descriptor(sim_engine, storage_snapshot, state_snapshot_id):
        original_restore(sim_engine, storage_snapshot, state_snapshot_id)
        active_address = "0x" + sim_engine.vm._contract_address.hex()
        manager = sim_engine._storages.get(active_address)
        contract_cls = sim_engine._classes.get(active_address)
        if manager is not None and contract_cls is not None:
            from genlayer.storage import Root

            sim_engine.vm._storage = manager
            Root.MANAGER = manager
            instance = loader._allocate_contract(contract_cls, sim_engine.vm)
            sim_engine._instances[active_address] = loader._make_contract_proxy(instance)

    monkeypatch.setattr(sim_consensus, "_restore_storages", restore_storage_and_contract_descriptor)

    try:
        address, _ = engine.deploy(
            "contracts/consensus_guard.py",
            sender="0x0000000000000000000000000000000000000001",
        )
        engine.vm.sender = "0x0000000000000000000000000000000000000002"
        for url, body in zip(URLS, BODIES, strict=True):
            engine.vm.mock_web(
                re.escape(url),
                {"status": 200, "body": body.decode("utf-8")},
            )
        engine.vm.mock_llm(
            "evidence classifier inside a smart contract",
            json.dumps({"labels": ["SUPPORTS", "SUPPORTS"]}),
        )

        case_id = engine.call_method(
            address,
            "open_case",
            [
                "glsim-five-vote",
                "Was release 4.2 published on 2026-10-10?",
                "Use only explicit release dates in the evidence.",
                _manifest(),
                2,
            ],
        )

        def execute():
            result = engine.call_method(address, "resolve", [case_id])
            return result, encode_result_bytes(result)

        consensus = sim_consensus.run_consensus(
            engine, execute, num_validators=5, max_rotations=3
        )
        case = json.loads(engine.call_method(address, "get_case", [case_id]))
        decision_count = engine.call_method(address, "decision_count")
        latest = None
        if decision_count:
            latest = json.loads(engine.call_method(address, "get_latest_decision", [case_id]))
        return consensus, case, decision_count, latest, len(engine.vm._captured_validators)
    finally:
        engine.deactivate()


def test_glsim_contract_smoke_uses_no_callback_auto_agree_path(monkeypatch):
    consensus, case, decision_count, latest, captured_count = _run_consensus_case(monkeypatch)

    assert consensus.status.value == "FINALIZED"
    assert consensus.votes == ["agree"] * 5
    assert consensus.rotation == 0
    assert consensus.result == "VERIFIED"
    assert case["state"] == "DECIDED"
    assert decision_count == 1
    assert latest["outcome"] == "VERIFIED"
    assert captured_count == 1


def test_glsim_runner_restores_state_after_permanent_simulated_dissent(monkeypatch):
    class FakeEngine:
        def __init__(self):
            self._storages = {"contract": {"decision_count": 0}}
            self.vm = SimpleNamespace(_captured_validators=[], _storage={"slot": 0})
            self._instances = {}
            self._classes = {}

        def create_snapshot(self):
            return copy.deepcopy(self._storages)

        def restore_snapshot(self, snapshot):
            self._storages = copy.deepcopy(snapshot)
            return True

    engine = FakeEngine()
    monkeypatch.setattr(
        sim_consensus,
        "_run_validators",
        lambda vm, captured, num_validators: ["disagree"] * num_validators,
    )

    def execute():
        engine._storages["contract"]["decision_count"] += 1
        engine.vm._captured_validators.append((1, lambda: 1, lambda result: False))
        return 1, b"1"

    result = sim_consensus.run_consensus(engine, execute, num_validators=5, max_rotations=3)

    assert result.status.value == "UNDETERMINED"
    assert result.votes == ["disagree"] * 5
    assert result.rotation == 2
    assert engine._storages["contract"]["decision_count"] == 0


def test_glsim_contract_disagreement_does_not_store_decision(monkeypatch):
    monkeypatch.setattr(
        sim_consensus,
        "_run_validators",
        lambda vm, captured, num_validators: ["disagree"] * num_validators,
    )
    consensus, case, decision_count, latest, _captured_count = _run_consensus_case(monkeypatch)

    assert consensus.status.value == "UNDETERMINED"
    assert consensus.votes == ["disagree"] * 5
    assert consensus.rotation == 2
    assert case["state"] == "OPEN"
    assert decision_count == 0
    assert latest is None
