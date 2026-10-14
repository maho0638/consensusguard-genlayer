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


URL_A = "https://evidence-a.example.com/report.txt"
URL_B = "https://evidence-b.example.com/report.txt"
# GenVM validates TLDs BEFORE consulting mock_web_response; .example is
# rejected as TLD_FORBIDDEN. .com domains work with these exact mocked URLs.
BODY_A = "The signed release manifest states version 4.2 was published on 2026-10-10."
BODY_B = "The official changelog lists version 4.2 with release date 2026-10-10."


def _manifest():
    sources = []
    for url, body in ((URL_A, BODY_A), (URL_B, BODY_B)):
        sources.append(
            {"url": url, "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()}
        )
    return json.dumps(sources, separators=(",", ":"))


def test_studio_disagreement_rollback_and_recovery():
    """Five-validator local Studio dissent, rollback and recovery; no GLSim."""
    from gltest import get_contract_factory, get_validator_factory, get_gl_client
    from gltest.assertions import tx_execution_succeeded

    llm_response = {
        "nondet_exec_prompt": {
            "evidence classifier inside a smart contract":
                '{"labels":["SUPPORTS","SUPPORTS"]}',
            # GenVM mock matcher supports the empty key as a safe default.
            # Never fall through to an unavailable real API in isolated CI.
            "": '{"labels":["SUPPORTS","SUPPORTS"]}'
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


    # Phase 4: three mutually exclusive, valid classifier results. No one
    # result is held by a majority of five nodes (2 SUPPORTS, 2 REFUTES,
    # 1 UNCLEAR). Whichever validator becomes leader must face dissent.
    import time
    from collections import Counter
    factory_v = get_validator_factory()
    web_mock = {
        "nondet_web_request": {
            URL_A: {"method": "GET", "status": 200, "body": BODY_A},
            URL_B: {"method": "GET", "status": 200, "body": BODY_B},
        }
    }
    labels = ["SUPPORTS", "SUPPORTS", "REFUTES", "REFUTES", "UNCLEAR"]
    dissent_configs = []
    for label in labels:
        answer = json.dumps({"labels": [label, label]}, separators=(",", ":"))
        dissent_configs.append(factory_v.create_mock_validator(
            mock_llm_response={"nondet_exec_prompt": {
                "evidence classifier inside a smart contract": answer,
                "": answer,
            }},
            mock_web_response=web_mock,
        ).to_dict())
    replaced = local_client.provider.make_request("sim_replaceValidators", [dissent_configs])
    assert not replaced.get("error"), "Cannot configure independently dissenting validators"
    configured = replaced.get("result", [])
    assert isinstance(configured, list) and len(configured) == 5
    address_set = {str(c.get("address", "")).lower() for c in configured}
    assert len(address_set) == 5
    assert int(local_client.provider.make_request("sim_countValidators", [])["result"]) == 5
    print("PHASE4_READY: five validators, 2/2/1 conflicting responses", flush=True)

    before = json.loads(contract.get_case(args=[0]).call())
    assert before["state"] == "OPEN" and before["latest_decision_id"] == -1
    assert contract.case_count().call() == 1
    assert contract.decision_count().call() == 0
    recorded = []
    original_audited_wait = local_client.wait_for_transaction_receipt

    def _track_wait(*args, **kwargs):
        tx_hash = kwargs.get("transaction_hash", args[0] if args else None)
        if tx_hash:
            recorded.append(str(tx_hash))
        return original_audited_wait(*args, **kwargs)

    local_client.wait_for_transaction_receipt = _track_wait

    print("PHASE4_DISAGREEMENT_START", flush=True)
    dissent_receipt = None
    try:
        dissent_receipt = contract.resolve(args=[0]).transact(
            transaction_context=phase1_context,
            consensus_max_rotations=3,
            fees=fees,
            wait_until="finalized",
            wait_retries=80,
        )
        print("PHASE4_WAIT_RETURNED", flush=True)
    except Exception as exc:
        print("PHASE4_WAIT_EXCEPTION_CLASS:", type(exc).__name__, flush=True)
    assert recorded, "No submitted transaction hash was captured"
    tx_hash = recorded[-1]
    assert tx_hash.startswith("0x") and len(tx_hash) == 66
    print("PHASE4_DISAGREEMENT_TX:", tx_hash, flush=True)

    # The SDK's get_transaction() can omit receipt/status fields; do not
    # misclassify that as UNKNOWN after a successful finalized waiter.
    # The transact() return value IS the consensus receipt when available.
    tx = dissent_receipt if isinstance(dissent_receipt, dict) else {}
    print("PHASE4_RECEIPT_KEYS:", ",".join(sorted(
        k for k in tx if isinstance(k, str) and k.isidentifier()
    )), flush=True)
    raw_status = tx.get("status_name", tx.get("status", "UNKNOWN"))
    status = str(getattr(raw_status, "value", raw_status)).upper()
    consensus = tx.get("consensus_data", {}) or {}
    votes = consensus.get("votes", {}) or {}
    counts = Counter(str(v).lower() for v in votes.values()) if isinstance(votes, dict) else Counter()
    print("PHASE4_RECEIPT_STATUS:", status, flush=True)
    print("PHASE4_CONSENSUS_KEYS:", ",".join(sorted(
        k for k in consensus.keys() if isinstance(k, str) and k.isidentifier()
    )), flush=True)
    print("PHASE4_VOTES: agree=" + str(counts["agree"]) +
          " disagree=" + str(counts["disagree"]) +
          " idle=" + str(counts["idle"]) +
          " other=" + str(sum(n for k,n in counts.items() if k not in ("agree","disagree","idle"))),
          flush=True)
    current_case = json.loads(contract.get_case(args=[0]).call())
    current_decisions = int(contract.decision_count().call())
    print("PHASE4_CHAIN_STATE: state=" + current_case["state"] +
          " decisions=" + str(current_decisions), flush=True)
    if status == "UNKNOWN":
        # Explicitly request the protocol status, never default to UNKNOWN
        # and claim a rollback based solely on a missing field.
        try:
            status_rpc = local_client.provider.make_request(
                "gen_getTransactionStatus", [{"txId": tx_hash}]
            )
            data = status_rpc.get("result")
            if isinstance(data, dict):
                status = str(data.get("status", "UNKNOWN")).upper()
            print("PHASE4_RPC_STATUS:", status, flush=True)
        except Exception as exc:
            print("PHASE4_RPC_EXCEPTION_CLASS:", type(exc).__name__, flush=True)
    # This GenLayer Studio build can finalize a receipt after consensus has
    # rejected a proposed state. FINALIZED means the transaction lifecycle
    # ended; it does not mean the candidate state was committed. The decisive
    # safety checks below independently require real dissent + unchanged
    # committed on-chain state, not status alone.
    assert status in ("FINALIZED", "UNDETERMINED"), (
        "Transaction has not reached a terminal, independently checkable status"
    )
    # get_transaction() returns the FULL localnet receipt. The SDK's
    # wait_for_transaction_receipt(full_transaction=False) deliberately strips
    # consensus_history and rotation_count from its simplified receipt.
    # Check rotation proof from full JSON-RPC state instead of relying on the
    # simplified transact() return above.
    full_tx = local_client.get_transaction(transaction_hash=tx_hash)
    assert isinstance(full_tx, dict), "No full on-chain transaction available"
    history = full_tx.get("consensus_history", {}) or {}
    assert isinstance(history, dict), "Full receipt has no consensus history"
    rounds = history.get("consensus_results", [])
    assert isinstance(rounds, list), "Unexpected consensus history structure"
    safe_rounds = [
        str(row.get("consensus_round", ""))[:50]
        for row in rounds if isinstance(row, dict)
    ]
    print("PHASE4_HISTORY_ROUNDS:", ",".join(safe_rounds), flush=True)
    rotation = full_tx.get("rotation_count")
    print("PHASE4_ROTATION_COUNT:", rotation if isinstance(rotation, int) else "UNAVAILABLE", flush=True)
    assert rotation == 0, "A five-member full committee unexpectedly rotated with no spare validator"
    assert "Undetermined" in safe_rounds, "No terminal Undetermined consensus history"
    print("PHASE4_NO_SPARE_ROTATION: count=0 terminal=Undetermined", flush=True)
    # Explicit round history, if returned, must not show a positive agreement.
    assert not any("Accepted" == n for n in safe_rounds), (
        "Conflict transaction history unexpectedly records a majority accept"
    )
    assert isinstance(votes, dict) and len(votes) == 5
    assert {str(a).lower() for a in votes} == address_set
    assert counts["disagree"] >= 3, "Need an actual three-validator rejecting majority"
    assert counts["agree"] < 3, "Contradictory majority was unexpectedly committed"
    # Check actual ledger state, not only a receipt or Python model.
    after = json.loads(contract.get_case(args=[0]).call())
    assert after == before, "Dissent transaction mutated persisted case"
    assert contract.case_count().call() == 1
    assert contract.decision_count().call() == 0
    print("PHASE4_ROLLBACK_STATE: OPEN decisions=0 case_unchanged=true", flush=True)

    # Recovery: same immutable case and manifest, but now matching validator
    # mocks. The system must be able to reach a valid final decision.
    healthy_answer = '{"labels":["SUPPORTS","SUPPORTS"]}'
    healthy = factory_v.batch_create_mock_validators(
        count=5,
        mock_llm_response={"nondet_exec_prompt": {
            "evidence classifier inside a smart contract": healthy_answer,
            "": healthy_answer,
        }},
        mock_web_response=web_mock,
    )
    restored = local_client.provider.make_request(
        "sim_replaceValidators", [[v.to_dict() for v in healthy]]
    )
    assert not restored.get("error")
    assert isinstance(restored.get("result"), list) and len(restored["result"]) == 5
    print("PHASE4_RECOVERY_START", flush=True)
    resolved = contract.resolve(args=[0]).transact(
        transaction_context=phase1_context,
        consensus_max_rotations=3,
        fees=fees,
        wait_until="finalized",
        wait_retries=90,
    )
    assert tx_execution_succeeded(resolved), "Healthy retry did not execute"
    case = json.loads(contract.get_case(args=[0]).call())
    assert case["state"] == "DECIDED" and case["latest_decision_id"] == 0
    assert contract.decision_count().call() == 1
    decision = json.loads(contract.get_latest_decision(args=[0]).call())
    assert decision["outcome"] == "VERIFIED" and decision["support_count"] == 2
    assert case["manifest_sha256"] == before["manifest_sha256"]
    print("PHASE4_RECOVERY_TX:", recorded[-1], flush=True)
    print("PHASE4_RECOVERY_STATE: DECIDED decisions=1 outcome=VERIFIED", flush=True)
    print("PHASE4_COMPLETE: REAL_STUDIO_DISAGREEMENT_ROLLBACK_RECOVERY_PASS", flush=True)
