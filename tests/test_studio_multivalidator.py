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

    # v0.123 Studio requires a valid fee distribution even on disposable localnet.
    # Use the official SDK fee quote rather than changing the production contract.
    local_client = get_gl_client()
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
        transaction_context=transaction_context,
        consensus_max_rotations=3,
        fees=fees,
    )

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
        transaction_context=transaction_context,
        consensus_max_rotations=3,
        fees=fees,
    )
    print("STUDIO_PHASE: OPEN_RECEIPT")
    assert tx_execution_succeeded(opened), "open_case execution failed"
    assert contract.case_count().call() == 1

    case_id = 0
    resolved = contract.resolve(args=[case_id]).transact(
        transaction_context=transaction_context,
        consensus_max_rotations=3,
        fees=fees,
    )
    print("STUDIO_PHASE: RESOLVE_RECEIPT")
    assert tx_execution_succeeded(resolved), "resolve execution failed"

    case = json.loads(contract.get_case(args=[case_id]).call())
    decision = json.loads(contract.get_latest_decision(args=[case_id]).call())
    assert case["state"] == "DECIDED"
    assert case["latest_decision_id"] == 0
    assert decision["outcome"] == "VERIFIED"
    assert decision["support_count"] == 2
    assert decision["verified_count"] == 2
