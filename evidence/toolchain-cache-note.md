# Final verification environment note

Verification date: 2026-10-12.

- The first pytest rerun could not start contract tests: the Direct Mode SDK
  loader had no cached GenVM runner and the sandbox blocked the HTTPS socket
  needed to fetch it. This failed attempt is not counted as a test result.
- The pinned public test runner bundle `v0.6.0-rc9` was then fetched into the
  local test cache. The final captured run is `pytest.log`: **66 passed, 1
  skipped**.
- The linter attempted to write its cache under `/root/.cache`, which is
  read-only here. The linter was rerun with its cache redirected to a writable
  project-local `.tool-home` directory; that cache is excluded from the ZIP.
- The linter did not publish a bundle matching `v0.6.0-rc9`. Its official
  release discovery selected `v0.3.0-rc7`; `genvm-lint check` passed (3 AST
  checks and semantic validation for 8 methods), with an `I200` warning that a
  newer runner is available. The linter semantic result is therefore tied to
  that bundle, not proof of compatibility with `v0.6.0-rc9`.
- A direct attempt to feed the test runner's `v0.6.0-rc9` bundle into the
  linter cache also failed: `genvm-linter==0.11.0` expects a different archive
  layout and reported its expected `runners/py-genlayer/...tar` entry missing.
  The exact diagnostic is preserved in `linter-v06-bundle-attempt.md`.
- `genvm-lint typecheck` passed with zero diagnostics; `compileall` and `pip
  check` passed. Their captured output is in the adjacent logs.
- Direct Mode tests enable strict serialization checks: both nondeterministic
  closures must survive `cloudpickle.dumps`/`loads` and remain callable. The
  first focused attempt exposed the missing test dependency; after pinning
  `cloudpickle==3.1.2`, the focused and complete test suites passed.
- During the final recheck, one diagnostic invocation pointed `HOME` at an
  empty `/tmp` cache; network access was denied and lint/typecheck could not
  load their SDK bundle. The commands were rerun against the already populated
  project-local cache and passed; these cache-path failures are not treated as
  passing checks.
- Studio multi-validator execution remains unrun because the local Studio,
  container runtime, and socket binding are unavailable. The skipped test is
  not represented as a success.


After this historical note was written, one temporary shell invocation again used the read-only global HOME and another lacked the virtualenv bin on PATH. The final verification re-used the project-local SDK cache, set PATH correctly for pyright, reran the complete suite and all static checks, and captured final outputs in `final-run-environment.log`. The final hashes and test counts are recorded there.

## Studio investigation and final package refresh

The Work Cloud Browser investigation and observed schema RPC error are
documented in `studio-dev-schema-investigation.md`. The linter archive cache
was found truncated during the final bundle check, replaced from the official
release artifact, decompressed for integrity with `xz -t`, and then matched
the locked SHA-256. A final local rerun after the public `u256` schema fix
completed with 66 passed and one opt-in Studio integration skipped. See the
refreshed `pytest.log`, `genvm-lint-*.log`, `typecheck-attempt.log`,
`pip-check.log`, and `toolchain-bundle-check.log`.
