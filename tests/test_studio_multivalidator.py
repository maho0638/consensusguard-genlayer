"""Opt-in GenLayer Studio integration test with five mock validators.

This test uses GenLayer Test's Studio mode over JSON-RPC. It is deliberately
opt-in so normal offline pytest runs never contact a node or submit a write.
"""

import hashlib
import json
import os
from pathlib import Path

import pytest


RUN_STUDIO = os.environ.get("CONSENSUSGUARD_RUN_STUDIO") == "1"
pytestmark = pytest.mark.skipif(
    not RUN_STUDIO,
    reason="set CONSENSUSGUARD_RUN_STUDIO=1 to run against local GenLayer Studio",
)


URL_A = "https://evidence-a.example/report.txt"
URL_B = "https://evidence-b.example/report.txt"
BODY_A = "The signed release manifest states version 4.2 was published on 2026-10-10."
BODY_B = "The official changelog lists version 4.2 with release date 2026-10-10."


def _manifest():
    sources = []
    for url, body in ((URL_A, BODY_A), (URL_B, BODY_B)):
        sources.append(
            {"url": url, "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()}
        )
    return json.dumps(sources, separators=(",", ":"))


def test_studio_five_mock_validators_finalize_matching_evidence():
    """Five Studio validators independently re-fetch and re-classify inputs."""
    from gltest import get_contract_factory, get_validator_factory, get_gl_client
    from gltest.assertions import tx_execution_succeeded

    llm_response = {
        "nondet_exec_prompt": {
            "evidence classifier inside a smart contract":
                '{"labels":["SUPPORTS","SUPPORTS"]}'
        }
    }
    web_response = {
        "nondet_web_request": {
            URL_A: {"method": "GET", "status": 200, "body": BODY_A},
            URL_B: {"method": "GET", "status": 200, "body": BODY_B},
        }
    }
    validators = get_validator_factory().batch_create_mock_validators(
        count=5,
        mock_llm_response=llm_response,
        mock_web_response=web_response,
    )
    transaction_context = {
        "validators": [validator.to_dict() for validator in validators],
        "genvm_datetime": "2026-10-12T12:00:00Z",
    }

    # The phase-one deploy/open_case path performs deterministic state updates:
    # use the five persistent Studio validators rather than creating five
    # transaction-scoped virtual validators. Virtual validators force an LLM
    # module stop/start on entering AND leaving temporal_snapshot(), which
    # can delay release of the claimed transaction after ACCEPTED.
    # Subsequent resolve tests still use full mocks (only in phase two).
    # Both the isolated phase-one check and later full-flow tests must use
    # the five persistent Studio validators for deterministic deploy/open_case.
    # Mock validator overrides are reserved exclusively for resolve(), which
    # performs nondeterministic HTTP/LLM work.
    phase1_context = {"genvm_datetime": transaction_context["genvm_datetime"]}
    print("STUDIO_PHASE: PERSISTENT_FIVE_VALIDATORS", flush=True)

    # v0.123 Studio requires a valid fee distribution even on disposable localnet.
    # Use the official SDK fee quote rather than changing the production contract.
    local_client = get_gl_client()

    # Phase-1 instrumentation: only safe status fields, no validator configurations
    # or receipts in CI logs. Each wait is inspected before and after polling.
    original_wait = local_client.wait_for_transaction_receipt
    def _safe_status(tx_hash):
        try:
            tx = local_client.get_transaction(transaction_hash=tx_hash)
            value = tx.get("status_name", tx.get("status", "UNKNOWN"))
            return str(getattr(value, "value", value))
        except Exception as exc:
            return "RPC_READ_FAILED_" + type(exc).__name__
    def _audited_wait(*args, **kwargs):
        tx_hash = kwargs.get("transaction_hash", args[0] if args else "")
        print("STUDIO_SAFE_WAIT_START:", str(tx_hash)[:70],
              "status=", _safe_status(tx_hash),
              "target=", kwargs.get("wait_until", "decided"), flush=True)
        try:
            receipt = original_wait(*args, **kwargs)
        except Exception as exc:
            print("STUDIO_SAFE_WAIT_FAILURE:", str(tx_hash)[:70],
                  "status=", _safe_status(tx_hash),
                  "exception=", type(exc).__name__, flush=True)
            # Do not include the original exception text: it can contain
            # raw transaction receipts or validator private data.
            raise AssertionError(
                "Studio receipt wait failed; see safe status checkpoint"
            ) from None
        print("STUDIO_SAFE_WAIT_DONE:", str(tx_hash)[:70],
              "status=", _safe_status(tx_hash), flush=True)
        return receipt
    local_client.wait_for_transaction_receipt = _audited_wait
    rpc_chain_response = local_client.provider.make_request("eth_chainId", [])
    rpc_chain_id = int(rpc_chain_response["result"], 16)
    sdk_chain_id = int(local_client.chain.id)
    print("STUDIO_RPC_CHAIN_ID:", rpc_chain_id, "SDK_CLIENT_CHAIN_ID:", sdk_chain_id)
    assert rpc_chain_id == sdk_chain_id, (
        f"RPC/SDK network IDs mismatch: RPC={rpc_chain_id}, SDK={sdk_chain_id}"
    )
    validator_total = int(local_client.provider.make_request("sim_countValidators", [])["result"])
    print("LOCAL_STUDIO_VALIDATOR_COUNT:", validator_total)
    assert validator_total == 5, f"Expected exactly five initialized validators, got {validator_total}"
    print("STUDIO_PHASE: VALIDATORS_READY")
    quote = local_client.estimate_transaction_fees({
        "leaderTimeunitsAllocation": 100,
        "validatorTimeunitsAllocation": 200,
        "executionBudgetPerRound": 1_000_000_000_000_000,
        "totalMessageFees": 0,
        "appealRounds": 0,
        "rotations": [3],
    })
    assert isinstance(quote, dict) and "distribution" in quote and "feeValue" in quote
    fees = {"distribution": quote["distribution"], "feeValue": quote["feeValue"]}
    print("STUDIO_PHASE: FEES_QUOTED")

    contract_path = Path(__file__).resolve().parents[1] / "contracts" / "consensus_guard.py"
    factory = get_contract_factory(contract_file_path=contract_path)
    print("STUDIO_PHASE: DEPLOY_START")
    contract = factory.deploy(
        transaction_context=phase1_context,
        consensus_max_rotations=3,
        fees=fees,
        wait_until="finalized",
    )

    print("STUDIO_PHASE: DEPLOY_FINALIZED", flush=True)
    print("STUDIO_PHASE: DEPLOY_DONE")
    opened = contract.open_case(
        args=[
            "studio-five-validator",
            "Was release 4.2 published on 2026-10-10?",
            "Use only explicit release dates in the evidence.",
            _manifest(),
            2,
        ]
    ).transact(
        transaction_context=phase1_context,
        consensus_max_rotations=3,
        fees=fees,
        wait_until="finalized",
    )
    print("STUDIO_PHASE: OPEN_RECEIPT")
    assert tx_execution_succeeded(opened), "open_case execution failed"
    assert contract.case_count().call() == 1
    if os.environ.get("CONSENSUSGUARD_PHASE1_ONLY") == "1":
        print("STUDIO_PHASE: PHASE1_OPEN_CASE_PASS", flush=True)
        return

    # Phase 2: configure the already registered five independent validators
    # with canned HTTP/LLM answers. Do NOT use transaction-scoped overrides:
    # Studio v0.123.0-rc.7 can leave the worker blocked after ACCEPTED when
    # temporal_snapshot restores five temporary provider configurations.
    registry_response = local_client.provider.make_request("sim_getAllValidators", [])
    assert not registry_response.get("error"), "Cannot inspect registered Studio validators"
    registered = registry_response.get("result", [])
    assert isinstance(registered, list) and len(registered) == 5
    addresses = [v.get("address") for v in registered]
    assert all(isinstance(x, str) and x.startswith("0x") for x in addresses)
    assert len(set(x.lower() for x in addresses)) == 5
    print("STUDIO_PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS", flush=True)

    # The test is isolated to disposable GitHub CI Studio containers.
    # No private keys are logged, and no hosted validator settings are touched.
    for i, validator in enumerate(registered):
        mock = validators[i].to_dict()
        response = local_client.provider.make_request(
            "sim_updateValidator",
            [
                validator["address"],
                int(validator.get("stake") or 1),
                mock["provider"],
                mock["model"],
                mock["config"],
                mock["plugin"],
                mock["plugin_config"],
            ],
        )
        assert not response.get("error"), (
            "Local mock validator configuration failed for ordinal " + str(i)
        )
        print("STUDIO_PHASE: REGISTERED_MOCK_" + str(i + 1), flush=True)

    assert int(local_client.provider.make_request("sim_countValidators", [])["result"]) == 5
    print("STUDIO_PHASE: FIVE_VALIDATOR_MOCKS_READY", flush=True)

    case_id = 0
    print("STUDIO_PHASE: RESOLVE_START", flush=True)
    resolved = contract.resolve(args=[case_id]).transact(
        transaction_context=phase1_context,
        consensus_max_rotations=3,
        fees=fees,
        wait_until="finalized",
        wait_retries=90,
    )
    print("STUDIO_PHASE: RESOLVE_FINALIZED", flush=True)
    assert tx_execution_succeeded(resolved), "resolve consensus execution failed"

    case = json.loads(contract.get_case(args=[case_id]).call())
    decision = json.loads(contract.get_latest_decision(args=[case_id]).call())
    assert case["state"] == "DECIDED"
    assert case["latest_decision_id"] == 0
    assert decision["outcome"] == "VERIFIED"
    assert decision["support_count"] == 2
    assert decision["verified_count"] == 2
    assert contract.decision_count().call() == 1
    assert decision["refute_count"] == 0
    assert decision["reason_code"] == "SUPPORT_THRESHOLD_MET"
    assert len(decision["source_results"]) == 2
    assert all(
        x["integrity"] == "VERIFIED" and x["label"] == "SUPPORTS"
        for x in decision["source_results"]
    )
    assert case["appeal_used"] is False
    print("STUDIO_PHASE: FIVE_VALIDATOR_RESOLVE_PASS", flush=True)

