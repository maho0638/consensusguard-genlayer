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


def test_studio_five_mock_validators_finalize_matching_evidence():
    """Five-validator Studio quorum: independently verify until decisive majority."""
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

    # GenLayer Studio integration tests use sim_replaceValidators to install
    # one complete mocked validator pool atomically (one provider restart).
    # Five consecutive sim_updateValidator calls would repeatedly restart
    # the LLM module and risk the exact phase-one worker stall.
    # This local replacement is safe: these are short-lived CI containers.
    configs = [validator.to_dict() for validator in validators]
    replaced = local_client.provider.make_request("sim_replaceValidators", [configs])
    assert not replaced.get("error"), "Atomic local five-validator setup failed"
    result = replaced.get("result")
    assert isinstance(result, list) and len(result) == 5
    configured_addresses = [v.get("address") for v in result]
    assert all(isinstance(v, str) and v.startswith("0x") for v in configured_addresses)
    assert len({v.lower() for v in configured_addresses}) == 5
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
    # Sanitize diagnostics: statuses and controlled enum categories only.
    # Never expose validator node_config, private keys, raw receipts, or calldata.
    leader_data = resolved.get("consensus_data", {}).get("leader_receipt", [])
    leader = leader_data[0] if isinstance(leader_data, list) and leader_data else {}
    def _enum_name(value):
        value = getattr(value, "value", value)
        return str(value)[:60] if value is not None else "none"
    print("STUDIO_RESOLVE_SAFE: status=" +
          _enum_name(resolved.get("status_name", resolved.get("status"))) +
          " execution=" +
          _enum_name(resolved.get("tx_execution_result_name", resolved.get("tx_execution_result"))) +
          " leader=" + _enum_name(leader.get("execution_result")) +
          " vote=" + _enum_name(leader.get("vote")), flush=True)
    debug_text = str(leader.get("genvm_result", {})).lower()[:50000]
    diagnostic_words = (
        "mock", "not found", "invalid", "json", "web", "http", "llm",
        "timeout", "response", "contract", "revert", "duplicate",
        "typeerror", "valueerror", "attributeerror", "failed",
        "insufficient", "missing", "keyerror", "exception",
    )
    print("STUDIO_RESOLVE_ERROR_MARKERS: " +
          ",".join(word for word in diagnostic_words if word in debug_text), flush=True)
    # Diagnostic is derived ONLY from the selected leader's local GenVM
    # error records. Never print validator identities or full receipts.
    genvm = leader.get("genvm_result")
    if isinstance(genvm, dict):
        vm_result = genvm.get("result")
        if isinstance(vm_result, str):
            try:
                vm_result = json.loads(vm_result)
            except (ValueError, TypeError):
                vm_result = {}
        if isinstance(vm_result, dict):
            allowed_kinds = {"USER_ERROR", "VM_ERROR", "RETURN", "PANIC", "INTERNAL_ERROR"}
            k = str(vm_result.get("kind", "")).upper()
            print("STUDIO_RESOLVE_VM_KIND: " + (k if k in allowed_kinds else "OTHER"), flush=True)
        diagnostics = genvm.get("genvm_log", [])
        error_lines = []
        for entry in diagnostics if isinstance(diagnostics, list) else []:
            if not isinstance(entry, dict):
                continue
            message = str(entry.get("message", ""))
            if any(word in message.lower() for word in (
                "error", "traceback", "exception", "panic",
                "invalid", "failed", "assertion", "attribute",
            )):
                import re
                scrub = message.splitlines()[-1][:340]
                scrub = re.sub(r"https?://[^\\s\"]+", "[URL]", scrub)
                scrub = re.sub(r"0x[0-9a-fA-F]{16,}", "[HEX]", scrub)
                scrub = re.sub(r"(?i)(api.key|token|password|secret|private.key)[^\\s,]*",
                               "[REDACTED]", scrub)
                scrub = re.sub(r"[^A-Za-z0-9 _./,:=()!?@\\[\\]-]", " ", scrub)
                if scrub.strip():
                    error_lines.append(scrub.strip()[:220])
        print("STUDIO_RESOLVE_VM_ERROR_COUNT: " + str(len(error_lines)), flush=True)
        for line in error_lines[-6:]:
            print("STUDIO_RESOLVE_VM_ERROR: " + line, flush=True)
    try:
        current_case = json.loads(contract.get_case(args=[case_id]).call())
        print("STUDIO_RESOLVE_SAFE_CASE_STATE: " +
              str(current_case.get("state", "unknown"))[:40], flush=True)
    except Exception as exc:
        print("STUDIO_RESOLVE_SAFE_CASE_STATE_ERROR: " +
              type(exc).__name__, flush=True)
    assert tx_execution_succeeded(resolved), "resolve consensus execution failed"
    # Studio v0.123 intentionally cancels unfinished validator tasks as soon
    # as a mathematically decisive quorum is reached (CommittingState).
    # Such validators receive synthetic IDLE receipts with error_code
    # CONSENSUS_VALIDATOR_QUORUM_REACHED; they did not independently vote.
    # Do not falsely demand unanimity or falsely count IDLE as agreement.
    from collections import Counter
    consensus = resolved.get("consensus_data", {}) or {}
    observed_votes = consensus.get("votes", {}) or {}
    independent_receipts = consensus.get("validators", []) or []
    assert isinstance(observed_votes, dict), "Missing consensus voting map"
    assert len(observed_votes) == 5, "Five eligible voter identities required"
    assert len(independent_receipts) == 4, "Four follower receipt slots required"
    expected_addresses = {v.lower() for v in configured_addresses}
    assert {str(addr).lower() for addr in observed_votes} == expected_addresses, (
        "Consensus voter identities do not match five configured validators"
    )
    counts = Counter(str(v).lower() for v in observed_votes.values())
    print("STUDIO_SAFE_VOTE_COUNTS: agree=" + str(counts["agree"]) +
          " idle=" + str(counts["idle"]) +
          " unexpected=" + str(sum(n for k, n in counts.items()
                                  if k not in ("agree", "idle"))), flush=True)
    assert set(counts).issubset({"agree", "idle"}), (
        "Validator disagreement/timeout is not a successful unanimous-mock quorum"
    )
    assert counts["agree"] >= 3, "Five-validator majority requires at least three agree votes"
    assert counts["agree"] + counts["idle"] == 5
    idle_receipts = [
        receipt for receipt in independent_receipts
        if isinstance(receipt, dict) and
        str(receipt.get("vote", "")).lower() == "idle"
    ]
    assert len(idle_receipts) == counts["idle"], (
        "Missing synthetic idle receipts for early quorum cancellations"
    )
    assert all(
        isinstance(receipt.get("genvm_result"), dict) and
        receipt["genvm_result"].get("error_code") ==
            "CONSENSUS_VALIDATOR_QUORUM_REACHED"
        for receipt in idle_receipts
    ), "IDLE must be proven to result from early quorum, not infrastructure failure"
    print("STUDIO_PHASE: FIVE_VALIDATOR_QUORUM_VERIFIED", flush=True)

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

