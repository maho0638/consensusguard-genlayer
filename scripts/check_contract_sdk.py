"""Load the contract against the exact pinned SDK and extract its ABI schema."""
import importlib.util
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

root = Path(__file__).resolve().parents[1]
sdk = root / "vendor/genvm/runners/genlayer-py-std/src"
os.environ.setdefault("GENERATING_DOCS", "true")
import numpy  # noqa: F401, E402 - SDK requires numpy registration first

wasi = MagicMock()
for name in ("storage_read", "storage_write", "get_balance", "get_self_balance", "gl_call"):
    setattr(wasi, name, MagicMock(return_value=None))
sys.modules["_genlayer_wasi"] = wasi
sys.path.insert(0, str(sdk))

path = root / "contracts/consensus_guard.py"
spec = importlib.util.spec_from_file_location("consensus_guard_schema_check", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from genlayer._internal.get_schema import get_schema

schema = get_schema(module.ConsensusGuard)
required = {"open_case", "resolve", "appeal", "case_count", "get_case", "get_decision", "get_latest_decision"}
missing = required - set(schema["methods"])
if missing:
    raise SystemExit(f"schema is missing public methods: {sorted(missing)}")
print(json.dumps({"ok": True, "sdk": "py-lib-genlayer-std:kzr02ndm9et4qkmbqpq5djjt5sme2yt76n7sz1qbzax0knt6mam0", "constructor": schema["ctor"], "methods": sorted(schema["methods"])}, sort_keys=True))
