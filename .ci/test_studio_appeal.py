"""Local five-validator state-machine appeal, opt-in ONLY; no public-chain transactions.
Executes original production contract unchanged using Studio v0.123.0-rc.7.
"""
import hashlib
import json
import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("CONSENSUSGUARD_RUN_STUDIO") != "1",
    reason="Explicit opt-in needed for LOCAL GenLayer Studio writes",
)

RECORDS = [
    ("https://appeal-evidence-a.example/source", "The signed release manifest confirms version 4.2."),
    ("https://appeal-evidence-b.example/source", "The official changelog confirms version 4.2."),
    ("https://appeal-round-a.example/source", "A later signed release manifest confirms version 4.2."),
    ("https://appeal-round-b.example/source", "The newer official changelog confirms version 4.2."),
]


def make_manifest(pairs):
    return json.dumps([
        {"url": url, "sha256": hashlib.sha256(body.encode()).hexdigest()}
        for url, body in pairs
    ], separators=(",", ":"))


def test_real_local_studio_appeal_finality_preserves_first_decision():
    from gltest import get_contract_factory, get_validator_factory, get_gl_client
    from gltest.assertions import tx_execution_succeeded

    quote = get_gl_client().estimate_transaction_fees({
        "leaderTimeunitsAllocation": 100,
        "validatorTimeunitsAllocation": 200,
        "executionBudgetPerRound": 1_000_000_000_000_000,
        "totalMessageFees": 0,
        "appealRounds": 0,
        "rotations": [3],
    })
    assert isinstance(quote, dict) and "distribution" in quote and "feeValue" in quote
    fees = {"distribution": quote["distribution"], "feeValue": quote["feeValue"]}

    web = {"nondet_web_request": {
        url: {"method": "GET", "status": 200, "body": body}
        for url, body in RECORDS
    }}
    llm = {"nondet_exec_prompt": {
        "evidence classifier inside a smart contract":
            '{"labels":["SUPPORTS","SUPPORTS"]}'
    }}
    validators = get_validator_factory().batch_create_mock_validators(
        count=5, mock_web_response=web, mock_llm_response=llm
    )
    ctx = {
        "validators": [v.to_dict() for v in validators],
        "genvm_datetime": "2026-10-12T12:00:00Z",
    }
    contract_path = Path.cwd() / "contracts" / "consensus_guard.py"
    assert contract_path.read_text(encoding="utf-8").startswith("# v0.3.0\n")
    contract = get_contract_factory(contract_file_path=contract_path).deploy(
        transaction_context=ctx, fees=fees, consensus_max_rotations=3,
        wait_until="finalized",
    )

    first = make_manifest(RECORDS[:2])
    second = make_manifest(RECORDS[2:])
    assert first != second

    opened = contract.open_case(args=[
        "audit-local-studio-appeal",
        "Did the release manifest document version 4.2?",
        "Require explicit version number 4.2 from both exact evidence bodies.",
        first, 2,
    ]).transact(transaction_context=ctx, fees=fees, consensus_max_rotations=3,
               wait_until="finalized")
    assert tx_execution_succeeded(opened), "open_case failed"
    assert contract.case_count().call() == 1

    resolved = contract.resolve(args=[0]).transact(
        transaction_context=ctx, fees=fees, consensus_max_rotations=3,
        wait_until="finalized")
    assert tx_execution_succeeded(resolved), "resolve failed"
    prior = json.loads(contract.get_latest_decision(args=[0]).call())
    case = json.loads(contract.get_case(args=[0]).call())
    assert case["state"] == "DECIDED"
    assert prior["round"] == 0 and prior["outcome"] == "VERIFIED"
    assert prior["verified_count"] == 2
    assert contract.decision_count().call() == 1

    appealed = contract.appeal(args=[0, second]).transact(
        transaction_context=ctx, fees=fees, consensus_max_rotations=3,
        wait_until="finalized")
    assert tx_execution_succeeded(appealed), "appeal failed"
    current = json.loads(contract.get_latest_decision(args=[0]).call())
    old = json.loads(contract.get_decision(args=[0]).call())
    case2 = json.loads(contract.get_case(args=[0]).call())
    assert contract.decision_count().call() == 2
    assert case2["state"] == "APPEALED"
    assert case2["appeal_used"] is True
    assert case2["latest_decision_id"] == 1
    assert current["round"] == 1 and current["outcome"] == "VERIFIED"
    assert current["support_count"] == 2 and current["verified_count"] == 2
    assert current["manifest_sha256"] != prior["manifest_sha256"]
    assert current["policy_sha256"] == prior["policy_sha256"]
    assert old == prior
    print("LOCAL_STUDIO_APPEAL_PASS: OPEN -> DECIDED -> APPEALED, two immutable decisions")
