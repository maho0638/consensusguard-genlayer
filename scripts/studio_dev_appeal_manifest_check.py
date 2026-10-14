#!/usr/bin/env python3
"""Check the ORIGINAL Studio Dev deploy against local code and prepare an appeal fixture.

READ ONLY. No funding, no private keys, no broadcast. Distinct sources and
their exact UTF-8 bytes are already documented in the 2026-10-12 readback.
"""
import base64, hashlib, json, os, urllib.request, urllib.error
from pathlib import Path

RPC="https://studio-dev.genlayer.com/api"
CONTRACT="0xBa84783D71d902c8BD3Ba63418Df172280249139"
urls=[
"https://httpbin.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQSBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu",
"https://httpbingo.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQiBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu",
]
sha=lambda b:hashlib.sha256(b).hexdigest()
sources=[]
for url in urls:
    body=base64.b64decode(url.rsplit("/",1)[-1],validate=True)
    sources.append({"url":url,"sha256":sha(body),"body":body})
assert sources[0]["sha256"]=="86ac284424d831f8799457c075295ea59bafb0c9a0d034e8859979b4a82e1609"
assert sources[1]["sha256"]=="1ae8c7be8b2c578b9b8b04130a4e62b6f96288fd30deb08aa2d5c5f81d056ece"
# Reverse order yields a distinct manifest commitment while keeping precisely
# the original human-validated evidence content. This checks one-appeal wiring,
# not an independent re-review of newly published evidence.
manifest=json.dumps([{"url":s["url"],"sha256":s["sha256"]} for s in sources[::-1]],separators=(",",":"))
new_hash=sha(manifest.encode())
original_hash="84f349ded38dfd428b3c83f35756bb4d1699ee90850a80e6f6f3577e8cd6fede"
assert new_hash!=original_hash
report=[
"# Studio Dev original deployed-code comparison and signed appeal preparation",
"",
"Run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/"+os.getenv("GITHUB_RUN_ID","unknown"),
"",
"All checks here are GET/JSON-RPC read-only; no wallet, GEN spend or transactions.",
"",
"## Pre-computed manifest",
"- Valid manifest entries: 2, normalized hosts distinct, lowercase SHA-256 exact.",
"- Earlier case manifest SHA-256: \`"+original_hash+"\`",
"- Proposed new normalized manifest SHA-256: \`"+new_hash+"\`",
"- Manifest reorder only: prior source texts and statuses remain unchanged; demonstrates case lifecycle only.",
"- Original test wallet signature is mandatory; requester-only contract authorization cannot be bypassed.",
"",
"\`\`\`json",
manifest,
"\`\`\`",
"",
"## Independent source HTTP retrieval",
]
for i,s in enumerate(sources):
    try:
        req=urllib.request.Request(s["url"],headers={"User-Agent":"ConsensusGuard-Readonly-Source-Verification/1.0"})
        with urllib.request.urlopen(req,timeout=16) as r: response=r.read(6500)
        ok=response==s["body"]
        report.append(f"- source {i+1}: HTTP byte integrity {'PASS' if ok else 'FAIL'}, bytes={len(response)}")
        print("APPEAL_SOURCE_VALID",i+1,ok,flush=True)
    except (Exception,) as exc:
        report.append(f"- source {i+1}: remote HTTP unavailable ({type(exc).__name__}); cannot assert present-time match")
        print("APPEAL_SOURCE_VALID",i+1,"UNREACHABLE",flush=True)
report.extend(["","## Historical deployed code"])
try:
    req=urllib.request.Request(RPC,headers={"Content-Type":"application/json"},
        data=json.dumps({"jsonrpc":"2.0","id":1,"method":"gen_getContractCode","params":[CONTRACT]}).encode())
    with urllib.request.urlopen(req,timeout=16) as r: res=json.loads(r.read(1_000_000))
    code=res.get("result")
    if not isinstance(code,str):
        report.append("- Studio Dev contract source: unavailable or unexpected response")
    else:
        try:
            deployed=base64.b64decode(code,validate=True)
            local=Path("contracts/consensus_guard.py").read_bytes()
            report.extend([
            "- Deployed source decoded successfully",
            f"- Deployed bytes: {len(deployed)}; local audited bytes: {len(local)}",
            f"- Deployed source SHA-256: \`{sha(deployed)}\`",
            f"- Current audit source SHA-256: \`{sha(local)}\`",
            "- Source comparison exact match: **"+str(deployed==local)+"**",
            ])
            print("DEPLOYED_CODE_MATCH_CURRENT_AUDIT:",deployed==local,flush=True)
        except Exception as exc:
            report.append("- Studio Dev deployed code decoding failed: "+type(exc).__name__)
except Exception as exc:
    report.append("- Studio Dev deployed code fetch unavailable: "+type(exc).__name__)

report+=["","## Signer and network boundary",
"1. The smart contract is requester-only and *only* the account that opened case 0 can sign a valid \`appeal\`.",
"2. The Studio Dev read RPC currently returns SQLAlchemy pending-rollback errors.",
"3. An appeal must not be represented as complete unless the transaction is \`FINALIZED\` and decisions are read back.",
"4. Do not submit the prepared manifest automatically, do not expose private keys or wallet recovery phrases.",
]
p=Path("evidence/STUDIO_DEV_APPEAL_MANIFEST_AND_DEPLOY_CODE_2026-10-14.md")
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text("\n".join(report)+"\n",encoding="utf-8")
print("AUDIT_REPORT",p)
