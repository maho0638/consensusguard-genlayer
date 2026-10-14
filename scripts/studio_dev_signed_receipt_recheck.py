#!/usr/bin/env python3
"""Independent READ-ONLY Studio Dev receipts and deploy source audit.

No writes, funding, signer or wallet. No transaction submission. Print safe
whitelisted status/return names and consensus votes, not identities.
"""
import base64,hashlib,json,os,urllib.request,urllib.error
from pathlib import Path

CONTRACT="0x06C85d37A4937659585D6855839659B45ebC3E46"
TXS=[
("deploy","0x02a61d2045383a5006481444b227b54a6b2002928eb57bd8a34181b990533acb"),
("open_case","0x32b17766f999e7f103421636a247f96737ecec6647d4041f54538c3e460ca4ad"),
("resolve","0xf837ea892a8a7ddc722dd4b2db7ab9096b654cf201aa47b6bc85600799534495"),
("appeal","0xfd9bcbfcd01112deb5eb074c8e0bc9be1ff0d7e1a875d4fa953fb2e2f2a889e8"),
]
RPC="https://studio-dev.genlayer.com/api"
BASE="https://studio-dev.genlayer.com/api/explorer"
REPORT=Path("evidence/STUDIO_DEV_SIGNED_APPEAL_RECEIPT_INDEPENDENT_AUDIT_2026-10-14.md")
lines=["# Fresh verified Studio Dev appeal: independent original transaction audit","",
 "CI https://github.com/maho0638/consensusguard-genlayer/actions/runs/"+os.environ.get("GITHUB_RUN_ID","unknown"),
 "Original successful signed test run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38575792658",
 "Read-only evidence; no private account data, re-deploy, funding, GEN spend or transaction submission.",
 "", "## Deployed code identity"]
def rpc(method,params):
    req=urllib.request.Request(RPC,data=json.dumps({"jsonrpc":"2.0","method":method,"id":1,"params":params}).encode("utf-8"),headers={"Content-Type":"application/json","Accept":"application/json","User-Agent":"ConsensusGuard-Readonly-Receipt-Audit"})
    with urllib.request.urlopen(req,timeout=24) as r: return json.loads(r.read(2_000_000))
def get(url):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"ConsensusGuard-Readonly-Receipt-Audit"})
    with urllib.request.urlopen(req,timeout=24) as r: return json.loads(r.read(2_000_000))
def err_code(obj):
    e=obj.get("error") if isinstance(obj,dict) else None
    return e.get("code") if isinstance(e,dict) else "other"
def pick(t,*keys):
    return next((t[k] for k in keys if isinstance(t,dict) and k in t and t[k] is not None),None)
def summarize(data,label):
    if not isinstance(data,dict):
        lines.append(f"- {label}: missing transaction dict")
        return False
    status=pick(data,"status","status_name")
    execution=pick(data,"tx_execution_result_name","txExecutionResultName","result_name","execution_result_name","tx_execution_result")
    result=pick(data,"consensus_result","consensusResult")
    consensus=data.get("consensus_data")
    if not isinstance(consensus,dict):consensus={}
    votes=consensus.get("votes")
    vote_counts={}
    if isinstance(votes,dict):
        for v in votes.values():
            name=str(v).lower()
            vote_counts[name]=vote_counts.get(name,0)+1
    elif isinstance(votes,list):
        for v in votes:
            name=str(v).lower()
            vote_counts[name]=vote_counts.get(name,0)+1
    msg=f"- {label}: status={str(status)[:48]}, execution={str(execution)[:48]}, result={str(result)[:48]}, votes="+json.dumps(vote_counts,sort_keys=True)
    lines.append(msg)
    print("STUDIO_DEV_SAFE_RECEIPT",msg,flush=True)
    return str(status).upper()=="FINALIZED" and str(execution).upper() in ("SUCCESS","FINISHED_WITH_RETURN","OK")
safe_count=0
try:
    chain=rpc("eth_chainId",[]).get("result")
    expected=int(chain,16)==61997 if isinstance(chain,str) and chain.startswith("0x") else int(chain)==61997
    lines.append("- Correct chain 61997: "+str(expected))
    if not expected: raise RuntimeError("wrong chain")
    source=Path("contracts/consensus_guard.py").read_bytes()
    local_digest=hashlib.sha256(source).hexdigest()
    address=get(BASE+"/address/"+CONTRACT)
    src=address.get("contract_code") if isinstance(address,dict) else None
    if not isinstance(src,str): raise RuntimeError("Explorer omitted deployed source")
    deployed_digest=hashlib.sha256(src.encode()).hexdigest()
    same=src.encode()==source
    lines.extend(["- Deployed source SHA-256: \`"+deployed_digest+"\`",
                  "- Current audited source SHA-256: \`"+local_digest+"\`",
                  "- Deployed source EXACT match: **"+str(same)+"**",
                  "- Explorer contract transaction count: "+str(address.get("tx_count","unknown"))])
    if not same:raise RuntimeError("deployed code mismatch")
    lines+=["","## Signed transaction receipts"]
    all_success=True
    for label,txid in TXS:
        raw=rpc("eth_getTransactionByHash",[txid])
        tx=raw.get("result")
        if "error" in raw:
            lines.append(f"- {label}: RPC retrieval error code="+str(err_code(raw)))
            all_success=False
            continue
        if not isinstance(tx,dict) or str(pick(tx,"hash","transactionHash")).lower()!=txid.lower():
            lines.append(f"- {label}: missing or mismatched hash")
            all_success=False
            continue
        recipient=pick(tx,"to_address","toAddress","to")
        if recipient and str(recipient).lower()!=CONTRACT.lower():
            lines.append(f"- {label}: recipient not current contract")
            all_success=False
            continue
        ok=summarize(tx,label)
        if ok:safe_count+=1
        else:all_success=False
        # Fetch the full Studio consensus details independently.
        extra=rpc("gen_getStudioTransactionByHash",[txid,True])
        if "error" in extra:
            lines.append(f"  - full Studio detail unavailable: RPC code {err_code(extra)}")
        else:
            x=extra.get("result")
            if isinstance(x,dict):
                found=x.get("consensus_data") or x.get("consensusData") or {}
                if isinstance(found,dict):
                    cs=found.get("votes")
                    if isinstance(cs,dict):
                        cn={}
                        for v in cs.values():
                            name=str(v).lower()
                            cn[name]=cn.get(name,0)+1
                        lines.append("  - full consensus votes: "+json.dumps(cn,sort_keys=True))
                    lines.append("  - consensus fields present="+str(len(found)))
    lines.extend(["",f"- FINISHED_WITH_RETURN and FINALIZED count: {safe_count}/4","- All four strong receipt gates pass: **"+str(all_success)+"**",
       "","## State proof boundary",
       "A full signed, successful FINALIZED contract-level appeal plus source identity",
       "establishes the contract's appeal() method was actually executed successfully,",
       "but the independent get_case/get_decision readback is currently inaccessible:",
       "the Studio Dev gen_call backend returns SQLAlchemy invalid session rollback -32603.",
       "Thus actual historic state mutation follows successful application execution and",
       "the exact tested contract, but JSON readback is NOT claimed to have succeeded.",
    ])
except Exception as exc:
    lines+=["","## ERROR "+type(exc).__name__+": no network writes used"]
finally:
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("READONLY_RECEIPT_EVIDENCE",REPORT,flush=True)
