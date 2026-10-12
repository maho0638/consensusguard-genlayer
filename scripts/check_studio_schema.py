"""Read-only schema RPC check. Never deploys, signs, funds or sends transactions."""
import argparse
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--code", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
code = args.code.read_bytes()
payload = {"jsonrpc": "2.0", "id": 1, "method": "gen_getContractSchemaForCode", "params": ["0x" + code.hex()]}
record = {"time_utc": datetime.now(timezone.utc).isoformat(), "endpoint": "https://studio-dev.genlayer.com/api", "source": str(args.code), "source_sha256": hashlib.sha256(code).hexdigest(), "request": payload}
try:
    request = urllib.request.Request(record["endpoint"], data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        record["http_status"] = response.status
        record["response"] = json.loads(response.read())
except Exception as exc:
    record["transport_error"] = repr(exc)
args.out.parent.mkdir(parents=True, exist_ok=True)
args.out.write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k:v for k,v in record.items() if k != "request"}, indent=2))
raise SystemExit(0 if "result" in record.get("response", {}) else 1)
