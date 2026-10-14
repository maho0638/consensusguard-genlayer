#!/usr/bin/env python3
"""Read-only Studio Dev fallback checks, no signing or transaction submission.
Inspect explorer materialized transaction/address views rather than gen_call.
"""
import json
import os
from pathlib import Path
import urllib.request
import urllib.error
from urllib.parse import quote

ADDR = "0xBa84783D71d902c8BD3Ba63418Df172280249139"
TX = "0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9"
RPC = "https://studio-dev.genlayer.com/api"
BASE = "https://explorer-studio-dev.genlayer.com"
MAX_RESPONSE = 2_000_000
report = [
  "# ConsensusGuard — Studio Dev non-GenVM contract and explorer read-only fallback",
  "",
  "Official Studio source: local tag v0.123.0-rc.7, endpoint implementations.",
  "CI https://github.com/maho0638/consensusguard-genlayer/actions/runs/"+os.environ.get("GITHUB_RUN_ID","unknown"),
  "No wallet secrets, no wallet signature, no GEN spending or transactions.",
  "",
]

def safe_error(err):
    if isinstance(err, dict):
        code=err.get("code","N/A")
        msg=str(err.get("message",""))
    else:
        code="N/A"; msg=str(err)
    # No user addresses or raw bodies are disclosed in evidence.
    if "reconnect until invalid transaction" in msg.lower():
        return str(code)+":SQLALCHEMY_INVALID_TRANSACTION_NEEDS_ROLLBACK"
    if "can't adapt type" in msg.lower():
        return str(code)+":INVALID_RPC_PARAMETER_TYPE"
    if "method not found" in msg.lower():
        return str(code)+":METHOD_UNSUPPORTED"
    return str(code)+":OTHER_ERROR"

def get_url(url):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"ConsensusGuard-RPC-diagnostic"})
    with urllib.request.urlopen(req,timeout=15) as resp:
        return json.loads(resp.read(MAX_RESPONSE))

def rpc(method,params,url=RPC):
    data=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode("utf-8")
    req=urllib.request.Request(url,data=data,headers={"Content-Type":"application/json",
                                                     "Accept":"application/json","User-Agent":"ConsensusGuard-RPC-diagnostic"})
    with urllib.request.urlopen(req,timeout=15) as resp:
        return json.loads(resp.read(MAX_RESPONSE))

def inspect(label,res):
    if not isinstance(res,dict):
        report.append(f"- {label}: unexpected JSON envelope")
        return None
    if "error" in res:
        report.append(f"- {label}: "+safe_error(res["error"]))
        return None
    val=res.get("result")
    if not val:
        report.append(f"- {label}: no result")
        return None
    if isinstance(val,list):
        report.append(f"- {label}: list length={len(val)}")
        return val
    if isinstance(val,dict):
        ks=list(val.keys())
        report.append(f"- {label}: result type=dict, field_count={len(ks)}")
        return val
    if isinstance(val,str):
        report.append(f"- {label}: text len={len(val)}, available=true")
        return val
    report.append(f"- {label}: result type={type(val).__name__}")
    return val

query=[
 ("RPC_contract_code", "gen_getContractCode", [ADDR]),
 ("RPC_contract_nonce", "gen_getContractNonce", [ADDR]),
 ("RPC_transactions_for_contract", "sim_getTransactionsForAddress", [ADDR]),
 ("RPC_transactions_for_contract_proxy", "sim_getTransactionsForAddress", [ADDR], BASE+"/api/rpc"),
 ("RPC_historical_complete", "gen_getStudioTransactionByHash", [TX,True]),
 ("RPC_historical_finalization", "gen_getTransactionStatus", [TX])
]
for args in query:
    label,method,params,*rest=args
    try:
        result=inspect(label,rpc(method,params,*rest))
        if method=="sim_getTransactionsForAddress" and isinstance(result,list):
            # Show only status/type per contract tx, never sender addresses.
            total=len(result)
            classes={}
            for item in result:
                if isinstance(item,dict):
                    type_ = str(item.get("type","unknown"))[:36]
                    status = str(item.get("status",item.get("result_name","unknown")))[:36]
                    key=type_+" / "+status
                    classes[key]=classes.get(key,0)+1
            report.append("  - transaction groups: "+json.dumps(classes,sort_keys=True))
            report.append("  - inspection_note: no actual appeal submitted can be assumed from txn count alone")
    except (Exception,) as e:
        report.append(f"- {label}: transport or decoding failure ({type(e).__name__})")

urls=[
 ("Explorer_address", BASE+"/api/address/"+ADDR),
 ("Explorer_contract", BASE+"/api/explorer/address/"+ADDR),
 ("Explorer_tx_page", BASE+"/api/transactions?address="+quote(ADDR)+"&limit=50"),
 ("Explorer_proxy_contract", BASE+"/api/explorer/contracts?search="+quote(ADDR)),
 ("Studio_server_contract", "https://studio-dev.genlayer.com/api/explorer/address/"+ADDR),
]
for label,url in urls:
    try:
        val=get_url(url)
        if isinstance(val,dict):
            obj=val.get("result",val)
            if isinstance(obj,dict):
                typ=obj.get("type","unknown")
                transactions=obj.get("transactions",obj.get("data"))
                length=len(transactions) if isinstance(transactions,(list,dict)) else 0
                report.append(f"- {label}: json OK, contract_type={str(typ)[:28]}, transaction_payload_count={length}")
                if isinstance(transactions,list):
                    summary={}
                    for item in transactions:
                        if isinstance(item,dict):
                            key=str(item.get("type","?"))[:25]+"/"+str(item.get("status","?"))[:25]
                            summary[key]=summary.get(key,0)+1
                    report.append("  - recent tx classes: "+json.dumps(summary,sort_keys=True))
            else: report.append(f"- {label}: unexpected dict wrapper")
        else: report.append(f"- {label}: JSON type={type(val).__name__}")
    except (Exception,) as e:
        code=getattr(e,"code",None)
        report.append(f"- {label}: error={type(e).__name__} http_code={code}")
report.extend([
  "",
  "## How to interpret",
  "The original contract-level appeal is not proven until a signed original-requester transaction is FINALIZED",
  "and the smart-contract state and both decisions are read back. An explorer transaction listing alone",
  "cannot prove app-level state. A local Studio result is not a live Studio Dev result.",
])
path=Path("evidence/STUDIO_DEV_ALTERNATIVE_READS_2026-10-14.md")
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text("\n".join(report)+"\n",encoding="utf-8")
print("\n".join(report))
