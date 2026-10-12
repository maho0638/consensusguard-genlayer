# Runner malformed root cause: source and artifact checks

Checked 2026-10-12 against the exact Studio Dev runner/SDK observed in browser logs.

## Reproduction

- Old contract runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.
- Current Studio runner: `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng`.
- The pinned SDK's `genlayer.gvm32.decode()` returns `None` for the old identifier (invalid/non-zero trailing padding) and 32 bytes for the current one. This matches the executor's checked conversion `Bytes32Hash::from_gvm32(&hash)`.
- The current executor maps that conversion failure to `invalid_contract runner malformed` before loading or executing the Python runner. Studio's old-runner probe log showed a 238-byte contract runner and no Python runner-load entry.
- With the current runner, Studio loaded the Python runner and its standard SDK, then successfully generated the complete eight-method schema.

## SDK compatibility changes

The old source used a legacy wildcard import/base class/storage decorator/nondeterministic call. The current standalone SDK API used by the fixed contract is `import genlayer as gl`, `gl.contract.Contract`, `@gl.storage.allow`, and `gl.vm.run_nondet`. The exact standard SDK archive is in `vendor/runners/py-lib-genlayer-std/`; the current Python runner archive is in `vendor/runners/py-genlayer/`.

## Source basis

- [Current executor source](https://github.com/genlayerlabs/genvm-executor/tree/49aa5746603f9a1b41a0144a87698de62a28282a): `executor/src/runners/mod.rs` parses runner identifiers and `executor/src/rt/supervisor/actions.rs` validates GVM32 and emits the malformed-runner error.
- [Runner documentation](https://sdk.genlayer.com/main/executors/v0.3/python-sdk/available-runners.html): lists the current `py-genlayer`, standard library, cloudpickle and CPython identities.
- [Manager release artifact](https://github.com/genlayerlabs/genvm-manager/releases/tag/v0.6.0-rc5): exact source bundle with SHA-256 in `toolchain.lock.json`.

The Studio GenVM log version (`v0.3.0-rc7`) and manager artifact release label (`v0.6.0-rc5`) belong to different version namespaces. We verified runner/SDK IDs and artifacts directly; we do not claim that those version labels are interchangeable.
