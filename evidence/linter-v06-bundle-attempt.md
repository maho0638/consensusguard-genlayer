# Attempted v0.6.0-rc9 semantic lint

Command: `GENVM_VERSION=v0.6.0-rc9 genvm-lint check contracts/consensus_guard.py --json`

Result: **not compatible with the linter's bundle reader** (exit code 1). The
GenVM Testing Suite bundle uses an archive layout that `genvm-linter==0.11.0`
does not understand as its cache format. The actual diagnostic was:

```json
{"ok":false,"lint":{"ok":true,"passed":3},"validate":{"ok":false,"errors":[{"code":"E101","msg":"Failed to load SDK: \"filename 'runners/py-genlayer/1j/b45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6.tar' not found\""}]}}
```

The Direct Mode and GLSim tests use the pinned `v0.6.0-rc9` bundle and pass.
For semantic lint and typecheck, CI pins the linter's own compatible bundle
`v0.3.0-rc7` and verifies its SHA-256 separately. That check passes but is not
represented as validation against the Direct Mode runner. This format mismatch
remains an explicit tooling limitation.
