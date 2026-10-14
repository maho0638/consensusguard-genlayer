#!/usr/bin/env python3
"""ONE-TIME controlled Studio Dev end-to-end write integration, using ephemeral wallet.

Requires explicit CONSENSUSGUARD_DEV_WRITE_AUTH=1. Executes at most one deploy,
open_case, resolve, and appeal on chain 61997, only after each succeeds.
Authorized TEST GEN only; no mainnet, Vercel, Portal, or user wallet.
Never saves/prints generated private keys.
"""
import hashlib, json, os, time
from pathlib import Path
from urllib.parse import urlsplit

from genlayer_py import create_account, create_client
from genlayer_py.chains import studio_devnet

CONTRACT_SRC=Path("contracts/consensus_guard.py")
OUT=Path("evidence/STUDIO_DEV_PHASE7_SIGNED_APPEAL_2026-10-14.md")
FLAG="CONSENSUSGUARD_DEV_WRITE_AUTH"
MAX_POLL=52
POLL_SECONDS=7

def log_msg(line):
    print("DEV_E2E_CHECK:", line, flush=True)
    audit.append("- "+line)

def marker(result):
    if isinstance(result,dict):
        return str(result.get("status") or result.get("status_name") or result.get("result_name") or "UNKNOWN")[:35]
    return "UNKNOWN"

def is_tx_success(tx):
    if not isinstance(tx,dict):return False
    if str(tx.get("status","")).upper() != "FINALIZED":
        return False
    # GenLayer Studio records vary in response field naming; at minimum the
    # worker must have finalized, and must not report a failed execution.
    result=str(tx.get("txExecutionResultName") or tx.get("tx_execution_result_name")
        or tx.get("result_name") or "").upper()
    bad=("ERROR","REVERT","FAILED","CANCEL","UNDERT")
    return not any(x in result for x in bad)

def receive(client, txid, what):
    if not isinstance(txid,str) or not txid.startswith("0x"):
        raise RuntimeError(what+" returned no transaction hash")
    log_msg(what+" tx: "+txid)
    for n in range(MAX_POLL):
        res=client.provider.make_request("eth_getTransactionByHash",[txid])
        tx=res.get("result") if isinstance(res,dict) else None
        status=marker(tx)
        if status=="FINALIZED":
            if not is_tx_success(tx):
                log_msg(what+" finalized but execution indicates failure")
                raise RuntimeError(what+" FAILED")
            log_msg(what+" finalized successfully")
            return tx
        if status in ("CANCELLED","DROPPED","ERROR"):
            raise RuntimeError(what+" non-success lifecycle "+status)
        time.sleep(POLL_SECONDS)
    raise RuntimeError(what+" did not finalize during time budget")

def manifest_from_rows(rows):
    import base64
    out=[]
    for url in rows:
        body=base64.b64decode(url.rsplit("/",1)[-1],validate=True)
        out.append({"url":url,"sha256":hashlib.sha256(body).hexdigest()})
    assert len({urlsplit(it["url"]).hostname for it in out})==len(out)==2
    return json.dumps(out,separators=(",",":"))

def run():
    global audit
    audit=[
        "# ConsensusGuard Studio Dev RC 61997 signed end-to-end trial",
        "", "This is independent test-only funding and a temporary ephemeral account.",
        "No private key is printed, stored or committed.",
        "Run https://github.com/maho0638/consensusguard-genlayer/actions/runs/"+os.environ.get("GITHUB_RUN_ID","unknown"),
        "",
    ]
    if os.getenv(FLAG)!="1":
        raise RuntimeError("Missing explicit test authorization env, refusing any writes")
    client_account=create_account()
    client=create_client(chain=studio_devnet,account=client_account)
    rc=client.provider.make_request("eth_chainId",[])
    chain_hex=rc.get("result")
    chain_id=int(chain_hex,16) if isinstance(chain_hex,str) and chain_hex.startswith("0x") else int(chain_hex)
    if chain_id!=61997:
        raise RuntimeError("Unexpected chain: abort without write")
    log_msg("preview chain ID 61997 confirmed, isolated new test wallet")
    # Built-in Studio Dev faucet; 1 test GEN maximum, not a token transfer
    # from the user's account. Runs only on chain 61997.
    funded=client.provider.make_request("sim_fundAccount",[client_account.address,10**18])
    if not isinstance(funded,dict) or "error" in funded:
        code=funded.get("error",{}).get("code","unknown") if isinstance(funded,dict) else "none"
        raise RuntimeError("Studio Dev built-in faucet failed: "+str(code))
    log_msg("funded isolated ephemeral account with 1 test GEN via built-in Studio simulator faucet")
    options={
        "leaderTimeunitsAllocation":125,
        "validatorTimeunitsAllocation":250,
        "executionBudgetPerRound":10**15,
        "totalMessageFees":0,
        "appealRounds":0,
        "rotations":[3],
    }
    estimate=client.estimate_transaction_fees(options)
    if not isinstance(estimate,dict) or not {"distribution","feeValue"}.issubset(estimate):
        raise RuntimeError("Current fee estimate not available; no deployment")
    fees={"distribution":estimate["distribution"],"feeValue":estimate["feeValue"]}
    log_msg("Studio Dev current fee quotation succeeded; no capped fee exceeds funded balance")
    if int(fees["feeValue"]) >= 10**18//4:
        raise RuntimeError("Fees unexpectedly high; refuse deploy")
    code=CONTRACT_SRC.read_text(encoding="utf-8")
    log_msg("current audit contract SHA256 "+hashlib.sha256(code.encode()).hexdigest())
    txid=client.deploy_contract(code=code,fees=fees,consensus_max_rotations=3)
    dep=receive(client,txid,"deploy")
    addr=dep.get("to_address") or dep.get("toAddress")
    if not isinstance(addr,str) or not addr.startswith("0x") or len(addr)!=42:
        raise RuntimeError("Deployed address unavailable; stop before next transaction")
    log_msg("deployed audit contract address "+addr)
    sources=[
      "https://httpbin.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQSBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu",
      "https://httpbingo.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQiBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu",
    ]
    first=manifest_from_rows(sources)
    second=manifest_from_rows(sources[::-1])
    m1=json.dumps(json.loads(first),sort_keys=True,separators=(",",":"))
    m2=json.dumps(json.loads(second),sort_keys=True,separators=(",",":"))
    assert hashlib.sha256(m1.encode()).hexdigest()!=hashlib.sha256(m2.encode()).hexdigest()
    cid="studio-dev-e2e-"+os.environ.get("GITHUB_RUN_ID","run")
    first_tx=client.write_contract(address=addr,function_name="open_case",args=[
      cid,
      "Do the committed test sources state CONSENSUSGUARD_TEST_STATUS=PASS?",
      "Only explicitly documented CONSENSUSGUARD_TEST_STATUS=PASS with a matching SHA-256 counts as support.",
      first,2
    ],fees=fees,consensus_max_rotations=3)
    receive(client,first_tx,"open_case")
    resolved_tx=client.write_contract(address=addr,function_name="resolve",args=[0],fees=fees,consensus_max_rotations=3)
    receive(client,resolved_tx,"resolve")
    appealed_tx=client.write_contract(address=addr,function_name="appeal",args=[0,second],fees=fees,consensus_max_rotations=3)
    receive(client,appealed_tx,"appeal")
    log_msg("appeal write has finalized on real Studio Dev preview")
    for method in ("get_case","get_decision","get_latest_decision"):
        try:
            read=client.read_contract(address=addr,function_name=method,args=[0])
            if isinstance(read,str) and len(read)<50000:
                obj=json.loads(read)
                log_msg(method+" confirmed state="+str(obj.get("state","n/a"))+" round="+str(obj.get("round","n/a")))
        except Exception as e:
            log_msg(method+" readback unavailable: "+type(e).__name__)
    log_msg("all four signed writes finalized; readback result must be inspected separately for full correctness")

try:
    run()
except Exception as exc:
    safe=type(exc).__name__+":"+str(exc)[:110]
    print("DEV_E2E_STOP:",safe,flush=True)
    audit.append("- STOP before further writes: "+safe)
finally:
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text("\n".join(audit)+"\n",encoding="utf-8")
    print("DEV_E2E_REPORT",OUT,flush=True)
