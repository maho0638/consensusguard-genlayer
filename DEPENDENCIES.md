# Runtime and toolchain versions

Recorded 2026-10-12. The contract now targets the runner demonstrated by Studio Dev's successful schema RPC.

| Component | Pinned version / identity |
|---|---|
| Python | 3.12.14 |
| GenLayer Testing Suite | `genlayer-test==0.30.0rc2` |
| Python SDK/client | `genlayer-py==0.19.0rc2` (test package) |
| GLSim | `0.30.0-rc.2` (included by test extra) |
| GenVM linter | `genvm-linter==0.11.0` |
| Pyright | locked in `requirements-lock.txt` |
| cloudpickle | `3.1.2` |
| Studio compatible Python runner | `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng` |
| Studio compatible standard SDK | `py-lib-genlayer-std:kzr02ndm9et4qkmbqpq5djjt5sme2yt76n7sz1qbzax0knt6mam0` |
| Source bundle | `genvm-manager v0.6.0-rc5`, SHA-256 in `toolchain.lock.json` |
| Executor source | `genlayerlabs/genvm-executor` commit `49aa5746603f9a1b41a0144a87698de62a28282a` |

The runner and SDK ZIP archives are included in `vendor/runners`; the SDK source is unpacked under `vendor/genvm/runners/genlayer-py-std/src` for schema extraction and Pyright. `python scripts/verify_toolchain_bundles.py` verifies the archived artifacts against the lock file. This avoids downloading a moving runtime during CI.

The Studio GenVM log identified runtime `v0.3.0-rc7`; the `v0.6.0-rc5` label above is the manager distribution that packages the exact GVM32 runner and SDK. These are different version namespaces. The previous `v0.6.0-rc9` CI artifact did not include Studio's runner hash, and is no longer the source of local test compatibility.

`genvm-lint lint` passes. Its semantic loader is not compatible with this SDK package path (`genlayer.py`); `scripts/check_contract_sdk.py` instead calls the exact SDK's schema extractor. Pyright runs against that source tree with documented dynamic-storage suppressions in `pyrightconfig.json`.
