#!/usr/bin/env python3
"""Non-broadcast read of the ORIGINAL Studio Dev contract via alternate execution RPCs.
No private keys, wallet signing, developer endpoints, transfers, or deploys.
"""
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

from genlayer_py.abi.calldata import encode
from genlayer_py.abi.transactions import serialize
from genlayer_py.contracts.utils import make_calldata_object

RPC = "https://studio-dev.genlayer.com/api"
RPC_PROXY = "https://explorer-studio-dev.genlayer.com/api/rpc"
CONTRACT="0xBa84783D71d902c8BD3Ba63418Df172280249139"
HISTORIC="0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9"
data=serialize([encode(make_calldata_object(method="get_case", args=[0])),b"\x00"])

def request(method,args,endpoint=RPC):
    body=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":args}).encode()
    req=urllib.request.Request(endpoint,data=body,headers={"Content-Type":"application/json","User-Agent":"CG-Readonly-Appeal-Diagnosis"})
    with urllib.request.urlopen(req,timeout=22) as r:return json.loads(r.read(1200000))

tx=request("eth_getTransactionByHash",[HISTORIC]).get("result") or {}
sender=tx.get("from_address") or tx.get("fromAddress") or tx.get("sender")
if not isinstance(sender,str) or not sender.startswith("0x") or len(sender)!=42:
    raise RuntimeError("Historical signed original sender unavailable; refuse alternate read from guess")
params={"type":"read","to":CONTRACT,"from":sender,"data":data}
cases=[
    ("gen_call_original_sender_latest_final","gen_call",[{**params,"transaction_hash_variant":"LATEST_FINAL"}]),
    ("gen_call_original_sender_status_finalized","gen_call",[{**params,"status":"finalized"}]),
    ("sim_call_original_sender_status_finalized","sim_call",[{**params,"status":"finalized"}]),
    ("eth_call_original_sender_finalized","eth_call",[{"from":sender,"to":CONTRACT,"data":data},"latest"]),
    ("explorer_rpc_proxy_gen_call","gen_call",[{**params,"status":"finalized"}],RPC_PROXY),
    ("explorer_rpc_proxy_sim_call","sim_call",[{**params,"status":"finalized"}],RPC_PROXY),
]
report=["# Alternate GenLayer execution RPC — original requester address; read-only",
    "",f"CI https://github.com/maho0638/consensusguard-genlayer/actions/runs/{os.getenv('GITHUB_RUN_ID','unknown')}",
    "Original sender pulled from finalized transaction; no account identity or private key logged.",
    "All type=read operations, no chain writes.",
    ""]
for label,method,args,*option in cases:
    try:
        ret=request(method,args,*option)
        if "error" in ret:
            error=ret["error"]
            if isinstance(error,dict):
                msg=str(error.get("message",""))
                code=error.get("code","unknown")
            else:
                code="unknown";msg=str(error)
            if "invalid transaction is rolled back" in msg or "Can't reconnect" in msg:
                category="SQLALCHEMY_UNROLLED_BACK_CONNECTION"
            elif "Method not found" in msg:
                category="METHOD_NOT_FOUND"
            elif "contract not found" in msg.lower():
                category="CONTRACT_NOT_FOUND"
            elif "invalid" in msg.lower():
                category="INVALID_CALL"
            else:
                category="OTHER_ERROR"
            report.append(f"- {label}: RPC_ERROR code={code} category={category}")
        else:
            result=ret.get("result")
            report.append(f"- {label}: result_present={result is not None}, result_type={type(result).__name__}")
            if isinstance(result,dict):
                status=result.get("status")
                report.append(f"  - status envelope type={type(status).__name__}")
    except Exception as e:
        report.append(f"- {label}: {type(e).__name__}; no broadcast")
report.append("\nCONTRACT-LEVEL APPEAL PROVEN? **NO** — only case-state inspection attempted.")
path=Path("evidence/STUDIO_DEV_ALTERNATIVE_GEN_CALL_2026-10-14.md")
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text("\n".join(report)+"\n",encoding="utf-8")
print("\n".join(report))
