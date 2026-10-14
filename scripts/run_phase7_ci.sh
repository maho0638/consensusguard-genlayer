#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/cg-phase7-qa
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python -m pip check 2>&1 | tee /tmp/cg-phase7-qa/pip_check.log
python scripts/verify_toolchain_bundles.py 2>&1 | tee /tmp/cg-phase7-qa/bundle_verify.log
python -m compileall -q contracts tests scripts 2>&1 | tee /tmp/cg-phase7-qa/compileall.log
genvm-lint lint contracts/consensus_guard.py --json 2>&1 | tee /tmp/cg-phase7-qa/genvm_lint.log
python scripts/check_contract_sdk.py 2>&1 | tee /tmp/cg-phase7-qa/contract_sdk.log
pyright -p pyrightconfig.json --outputjson 2>&1 | tee /tmp/cg-phase7-qa/pyright.log
pytest -q 2>&1 | tee /tmp/cg-phase7-qa/pytest.log
python scripts/build_phase7_package.py --qa-dir /tmp/cg-phase7-qa --destination package
python package/verify_sha256.py
python - <<'PY'
import json
from pathlib import Path
import subprocess
root=Path("package")
manifest=json.loads((root/"SHA256_MANIFEST.json").read_text())
recorded=set(manifest["files"])
actual={f.relative_to(root).as_posix() for f in root.rglob("*") if f.is_file()}-{"SHA256_MANIFEST.json"}
assert actual == recorded,"Final package inventory is incomplete"
assert manifest["source_git_commit"]==subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"Source commit mismatch"
print("PHASE7_COMPLETE_PACKAGE_CONTENT_VERIFIED")
print("PHASE7_MANIFEST_LISTED_FILES",len(recorded))
print("PHASE7_SOURCE_TRACKED_FILES",manifest["source_tracked_files"])
PY
