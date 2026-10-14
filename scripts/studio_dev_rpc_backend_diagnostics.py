#!/usr/bin/env python3
"""Non-mutating Studio Dev RPC cross-check; prints only diagnostic enums/counts."""
import json, os, re, socket, urllib.request, urllib.error
from pathlib import Path
TX="0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9"
ADDR="0xBa84783D71d902c8BD3Ba63418Df172280249139"
RPC="https://studio-dev.genlayer.com/api"
EXPLORER="https://explorer-studio-dev.genlayer.com/api/transactions/"+TX
CASES=[
    ("chain_identity","eth_chainId",[]),
    ("historical_transaction","eth_getTransactionByHash",[TX]),
    ("contract_storage_finalized","gen_getContractState",[{"address":ADDR,"status":"finalized"}]),
    ("contract_storage_accepted","gen_getContractState",[{"address":ADDR,"status":"accepted"}]),
    ("contract_schema_finalized","gen_getContractSchema",[{"address":ADDR,"status":"finalized"}]),
]
lines=["# 2026-10-14 Studio Dev RPC diagnostic — all read only",
       "",f"CI: https://github.com/maho0638/consensusguard-genlayer/actions/runs/{os.getenv('GITHUB_RUN_ID','unknown')}",
       "Studio Dev canonical RPC chain expected: 61997. No writes, wallet, test GEN or contract deploy.",
       "", "## Safe observations"]
def redact(msg):
    s=re.sub(r"0x[0-9a-fA-F]{16,}","[address/tx redacted]",str(msg))
    return s.replace("\n"," ")[:180]
def get(method,params):
    req=urllib.request.Request(RPC,
        data=json.dumps({"jsonrpc":"2.0","method":method,"params":params,"id":1}).encode(),
        headers={"Content-Type":"application/json","User-Agent":"ConsensusGuard-PhaseAppeal-Readonly"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.loads(r.read(1_000_000))
for label,method,params in CASES:
    try:
        res=get(method,params)
        if "error" in res:
            err=res["error"]
            lines.append(f"- {label}: ERROR code={err.get('code','unknown')} msg={redact(err.get('message',''))}")
            continue
        val=res.get("result")
        if label=="chain_identity":
            verified = (int(val,16)==61997) if isinstance(val,str) and val.startswith("0x") else (int(val)==61997)
            lines.append(f"- {label}: expected_chain_id_61997={verified}")
        elif label=="historical_transaction":
            ok = isinstance(val,dict) and str(val.get("hash","")).lower()==TX.lower()
            lines.append(f"- {label}: found={ok}; status={val.get('status','not in receipt') if isinstance(val,dict) else 'null'}")
        elif label.startswith("contract_storage"):
            bytes_length=len(bytes.fromhex(val.removeprefix("0x"))) if isinstance(val,str) else -1
            lines.append(f"- {label}: bytes={bytes_length}; present={bytes_length>0}")
        elif label=="contract_schema_finalized":
            methods = val.get("methods",{}) if isinstance(val,dict) else {}
            lines.append(f"- {label}: appeal_in_schema={'appeal' in methods}; method_count={len(methods)}")
    except (urllib.error.URLError,TimeoutError,socket.timeout,ValueError,TypeError,KeyError,OSError) as exc:
        lines.append(f"- {label}: ERROR {type(exc).__name__} {redact(str(exc))}")
try:
    req=urllib.request.Request(EXPLORER,headers={"Accept":"application/json","User-Agent":"ConsensusGuard-PhaseAppeal-Readonly"})
    with urllib.request.urlopen(req,timeout=20) as r:
        envelope=json.loads(r.read(1_000_000))
    tx=envelope.get("transaction",{}) if isinstance(envelope,dict) else {}
    lines.append("- explorer_historical_transaction: found="+str(isinstance(tx,dict) and str(tx.get("hash","")).lower()==TX.lower()))
except (urllib.error.URLError,TimeoutError,socket.timeout,ValueError,TypeError,OSError) as exc:
    lines.append("- explorer_historical_transaction: ERROR "+type(exc).__name__+" "+redact(str(exc)))
out=Path("evidence/STUDIO_DEV_RPC_BACKEND_DIAGNOSTICS_2026-10-14.md")
out.parent.mkdir(exist_ok=True,parents=True)
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("\n".join(lines))
