# Studio Dev schema investigation — corrected result

Date: 2026-10-12. Tested through the requested Work Cloud Browser at Studio Dev. No deploy, contract transaction, validator run, or GEN spend occurred.

## Result

Both a minimal `Probe` and the complete `contracts/consensus_guard.py` produced a schema in Studio Dev with runner `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng`. The full contract Run and Debug page displayed its constructor with no parameters and an enabled `Deploy consensus_guard.py` button. The returned schema lists the public methods `appeal`, `case_count`, `decision_count`, `get_case`, `get_decision`, `get_latest_decision`, `open_case`, and `resolve`. Studio's log UI truncates the encoded return value; the Run and Debug form itself confirms schema construction. A focused text record is in `evidence/schema-probes/studio-full-schema-success.txt`.

## Root cause

The previous contract pinned `py-genlayer:1jb45...`, a legacy runner ID. Studio Dev's current executor uses GVM32/Crockford Base32 runner hashes. Its source parser rejects the legacy ID as `invalid_contract runner malformed` before Python starts; the GenVM log showed a runner load of only 238 bytes and no Python runner load. This is a runner-ID format incompatibility, not a Studio schema service outage.

The contract also used the legacy SDK surface (`from genlayer import *`, `gl.Contract`, `@allow_storage`, and `gl.vm.run_nondet_unsafe`). The current SDK uses explicit `import genlayer as gl`, `gl.contract.Contract`, `@gl.storage.allow`, and `gl.vm.run_nondet`. Updating only the hash would therefore not have been a sufficient compatibility fix.

The GenVM runtime version printed by Studio was `v0.3.0-rc7`; `v0.6.0-rc9` is a GenVM Manager distribution release used by the testing suite, not the Studio runtime version. These version labels refer to different release tracks.

## Evidence and controls

- `schema-probes/old-version.txt`: old runner and SDK style; Studio returned `invalid_contract runner malformed` before Python execution.
- `schema-probes/new-version.txt`: minimal current-runner contract; schema succeeded.
- `schema-probes/new-no-version.txt`: confirms the runner header, rather than the optional `# v0.3.0` line, is decisive for the minimal probe.
- `schema-probes/studio-full-schema-success.txt`: full-contract Run and Debug schema state and runner-load evidence. Unrelated shared Studio log entries were excluded.
- `../contracts/consensus_guard.py`: migrated standalone source now pinned to the current runner/API.

The terminal's direct RPC request to Studio returned HTTP 403, so the schema check was performed in the requested browser UI. No alternate network route was attempted. Browser testing exercised schema generation only; it did not deploy or execute a transaction.

## Remaining gate

The local suite passes against the SDK archive whose runner ID exactly matches Studio. The real Studio multi-validator transaction remains unrun and requires explicit user approval before any deployment or GEN-consuming action.
