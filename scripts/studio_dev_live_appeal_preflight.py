#!/usr/bin/env python3
"""Phase-3 follow-up: inspect existing live Studio Dev contract READ ONLY.
No wallet/key, contract write, faucet, deploy, fee or token spending.
"""
import json
import os
from pathlib import Path

CONTRACT = "0xBa84783D71d902c8BD3Ba63418Df172280249139"
ORIGINAL_RESOLVE_TX = "0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9"
OUTPUT = Path("evidence/STUDIO_DEV_APPEAL_LIVE_PREFLIGHT_2026-10-14.md")

def unwrap(res):
    if isinstance(res, str):
        return json.loads(res)
    if isinstance(res, dict):
        return res
    raise RuntimeError(f"Read returned unexpected type: {type(res).__name__}")

def main():
    from genlayer_py import create_client
    from genlayer_py.chains import studio_devnet
    client = create_client(chain=studio_devnet)
    lines = [
        "# Studio Dev existing contract read-only appeal preflight",
        "",
        f"Contract: \`{CONTRACT}\`",
        f"Historical resolve: \`{ORIGINAL_RESOLVE_TX}\`",
        "Canonical preview: Studio Dev, chain ID 61997, not Studionet.",
        "All calls here are READ ONLY. No wallet, keys, GEN spend or tx broadcast.",
        "Workflow: https://github.com/maho0638/consensusguard-genlayer/actions/runs/"+os.environ.get("GITHUB_RUN_ID","unknown"),
        "",
    ]
    stage = "sdk-read_case"
    try:
        case = unwrap(client.read_contract(address=CONTRACT, function_name="get_case",args=[0],state_status="finalized"))
        stage = "sdk-read_latest_decision"
        decision = unwrap(client.read_contract(address=CONTRACT,function_name="get_latest_decision",args=[0],state_status="finalized"))
        stage = "sdk-read_case_count"
        case_count = client.read_contract(address=CONTRACT,function_name="case_count",args=[],state_status="finalized")
        stage = "sdk-read_decision_count"
        decision_count = client.read_contract(address=CONTRACT,function_name="decision_count",args=[],state_status="finalized")
        stage = "sdk-get_transaction"
        historic = client.get_transaction(hash=ORIGINAL_RESOLVE_TX)
        if not isinstance(historic,dict): historic={}
        original_sender = str(case.get("requester","")).lower()
        original_tx_sender = str(historic.get("from_address") or historic.get("sender") or "").lower()
        lines += ["## Live finalized read-back",
            "- RPC accessible: **YES**",
            "- Contract case \`0\` state: \`"+str(case.get("state"))+"\`",
            "- Appeal used: \`"+str(case.get("appeal_used"))+"\`",
            "- Decision outcome: \`"+str(decision.get("outcome"))+"\`",
            "- Case count: \`"+str(case_count)+"\`",
            "- Decision count: \`"+str(decision_count)+"\`",
            "- Historical tx sender matches case requester: "+str(bool(original_sender and original_sender==original_tx_sender)),
            "- Original requester wallet: **not disclosed or exported**",
        ]
        if case.get("state")=="APPEALED" and case.get("appeal_used") is True and int(case.get("latest_decision_id",-1)) == 1:
            lines+=["","**LIVE STUDIO DEV APPEAL IS ALREADY ONCHAIN.** Verify decision 0 and 1 to complete."]
            print("APPEAL_LIVE_STATE: ALREADY_APPEALED",flush=True)
            old=unwrap(client.read_contract(address=CONTRACT,function_name="get_decision",args=[0],state_status="finalized"))
            new=unwrap(client.read_contract(address=CONTRACT,function_name="get_decision",args=[1],state_status="finalized"))
            verified=(old.get("outcome")=="VERIFIED" and old.get("round")==0 and new.get("round")==1 and old.get("manifest_sha256") != new.get("manifest_sha256"))
            lines+=["- Append-only previous decision retained and new manifest committed: "+str(verified)]
            print("APPEAL_APPEND_ONLY_VALID: "+str(verified),flush=True)
        elif case.get("state")=="DECIDED" and case.get("appeal_used") is False:
            lines+=["","**BLOCKER: LIVE STUDIO DEV APPEAL HAS NOT BEEN SENT.**",
                    "The existing case's \`appeal\` write method is requester-only. Only the original"
                    " authorized Studio Dev requester wallet can sign and submit it.",
                    "SDK read-only client has no signing account; cannot legally impersonate requester.",
                    "User needs to select same original test account in Studio Dev and submit \`appeal(0,new_manifest_json)\`.",
                    "Contract source modification is NOT required; local Studio execution of the method was already proven."]
            print("APPEAL_LIVE_STATE: DECIDED_NEEDS_ORIGINAL_REQUESTER_SIGNATURE",flush=True)
        else:
            lines+=["","**BLOCKER: existing case is not in initial appealable state.**",
                    "Cannot assume a transaction will be possible without resolving current state."]
            print("APPEAL_LIVE_STATE: OTHER_"+str(case.get("state")),flush=True)
    except Exception as exc:
        import re
        msg = type(exc).__name__
        diagnostic = re.sub(r"0x[0-9a-fA-F]{16,}", "[hex redacted]", str(exc))[:240]
        lines+=["## RPC and state read",f"- Failed: \`{msg}\`","- Studio Dev preview may have reset or network may restrict GenVM read calls.","- No transaction was sent."]
        lines.append("- Failed stage: `" + stage + "`")
        lines.append("- SDK diagnostic (addresses redacted): `" + diagnostic + "`")
        print("APPEAL_READ_ERROR_TYPE:",msg,"STAGE:",stage,"CAUSE:",diagnostic,flush=True)
    OUTPUT.parent.mkdir(exist_ok=True,parents=True)
    OUTPUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("APPEAL_READ_ONLY_REPORT:",OUTPUT,flush=True)

if __name__=="__main__":
    main()
