"""Verify checked-in runner archives against the pinned toolchain manifest."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lock = json.loads((ROOT / "toolchain.lock.json").read_text())
for relative, expected in lock["artifacts"].items():
    path = ROOT / relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"SHA-256 mismatch: {relative}: {actual}")
    print(f"SHA-256 verified: {relative}")

runner = lock["runner"].split(":", 1)[1]
sdk = lock["sdk"].split(":", 1)[1]
if not any((ROOT / "vendor/runners/py-genlayer").glob(f"{runner[:2]}/{runner[2:]}.zip")):
    raise SystemExit("pinned GenVM runner archive is missing")
if not any((ROOT / "vendor/runners/py-lib-genlayer-std").glob(f"{sdk[:2]}/{sdk[2:]}.zip")):
    raise SystemExit("pinned GenLayer SDK archive is missing")
print(f"Pinned GenVM runner and SDK present: {lock['runner']}, {lock['sdk']}")
