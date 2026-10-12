# Final review run notes

This file distinguishes preliminary environment failures from the final
captured results. Failed attempts are not counted as successful tests.

- The first final test attempt found no GenVM `v0.6.0-rc9` archive in the
  temporary cache; the sandbox could not fetch it. The official release asset
  was then restored to the local cache and its SHA-256 matched
  `toolchain.lock.json`. The complete final pytest run passed afterward.
- The first linter check/typecheck invocation used the read-only `/root/.cache`
  location and did not load the SDK bundle. Subsequent invocations used the
  populated project-local `.tool-home` cache. Typecheck also required the
  project virtual environment's `bin` directory on `PATH` for the locked
  `pyright` executable. The final captured lint/check/typecheck runs completed
  as reported in their logs.
- A stale linter archive was found truncated during an earlier bundle check.
  The official `v0.3.0-rc7` runner archive was restored, validated, and matched
  its locked SHA-256. The final verifier output records both bundle matches.
- An exploratory duplicate-key LLM output test was not retained: the Direct
  Mode response-format mock decoded the structured JSON before the contract
  received it. Therefore no claim is made that duplicate keys in raw LLM
  transport text are rejected. Manifest JSON duplicate keys are separately
  rejected and tested.
- A forced GLSim dissent probe that covered only two of three rotations failed
  to establish rollback and remains excluded; the failed probe and corrected
  permanent-dissent coverage are in `exploratory-dissent-probe.md` and
  `glsim-disagreement-rollback.log`.
- The opt-in Studio test was not started against a Studio node. It is reported
  as skipped in `pytest.log`; no real multi-validator result is claimed.
