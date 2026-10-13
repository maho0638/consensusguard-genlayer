# Phase 1 — deterministic `open_case` timeout: isolated reproduction and correction

## Scope and result
**Project-level fix VERIFIED** on GenLayer Studio v0.123.0-rc.7, with five initialized Studio validators. The defect was in the phase-one *test transaction context*, not demonstrated in the production `open_case` contract source. Both deterministic writes now avoid unnecessary per-transaction virtual/mock validator reconfiguration.

This does **not** claim that GenLayer Studio's general-purpose virtual validator lifecycle is repaired. The original virtual/mock invocation remains reproducibly stalled in the pinned Studio version. The lower-level blocking operation within GenVM/LLM module reconfiguration was not independently traced; do not present that sub-cause as proven.

## Reproduction: original per-transaction five-mock context
- Legacy execution supplied `transaction_context["validators"]` for `deploy` and `open_case`, even though neither operation invokes external HTTP or LLM.
- The legacy Studio test produced `ACCEPTED` but did not reach `FINALIZED`. Extending the polling time from 150 to **270 seconds** did not change the outcome.
- In the controlled 270-second run, SQL diagnostics showed one `ACCEPTED` deployment; `blocked_at` remained set for 270 seconds, with a valid acceptance timestamp and an appeal deadline 240 seconds in the past. Zero finalization starts and zero successful transaction-processing completions were observed.
- The worker emitted 15 `Configuring validator` events. This is consistent with repeated mock-validator/LLM reconfiguration rather than contract execution remaining incomplete.
- Source-level mechanism: the pinned Studio worker enters `validators_manager.temporal_snapshot(virtual_validators)` when `transaction.sim_config.validators` is present. That context manager changes GenVM LLM providers on entry and restores the original providers on exit; the worker's claimed transaction is released only after its processing scope exits.
- The exact GenVM subcall responsible for the prolonged wait was **not isolated**, so attribution to a specific `/module/start` or `/module/stop` request would overstate the evidence.

Independent diagnostic run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38474606747
Reproduction with 270-second wait: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38474591242

Upstream Studio v0.123 source: `backend/consensus/worker.py` (virtual validator transaction path), `backend/validators/__init__.py` (`temporal_snapshot` lifecycle). No upstream files modified.

## Corrected project integration test
- For deterministic `deploy` and `open_case`, send `transaction_context = {"genvm_datetime": <fixed ISO datetime>}` **without** virtual validator overrides. This uses the already initialized five Studio validators and avoids dynamic LLM module reconfiguration.
- Assert exactly five Studio validators before execution; fee distribution quoted through the official SDK; check both transaction receipts at `wait_until="finalized"`; check `case_count() == 1`.
- Crucially, the correction applies to **both phase-one-only and future full-flow modes**. Only `resolve`, which actually needs mocked web/LLM results, retains the explicit virtual/mock context for subsequent testing.
- Clean CI run: **1 passed in 67.40s, exit 0**, two `FINALIZED` transactions, two successful worker finalizations, zero remaining blocked transactions, zero reported worker failures.
- On-chain behavior verified here is **local Studio test execution**, not Bradbury transactions, not an independent appeal/rollback test, and not proof that all five validators voted on both writes.

Corrected Studio run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38474767527
Quality run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38474767474 — **67 passed, 1 skipped**.
Audit test-fix commit: https://github.com/maho0638/consensusguard-genlayer/commit/7cb921429217ed4537f55ddbadde4fc7c19e2daa

## Change isolation
- Production contract `contracts/consensus_guard.py` is unchanged: Git blob SHA `149950eeb23550619a800ac6da96156c84108ccd` on `main` and on both isolated audit branches at verification time.
- No merge, Portal submission, Vercel deployment, production wallet transaction or contract amendment.
- **Phase-one project test-path issue: closed.** Separate actual nondeterministic `resolve` / appeal / disagreement validation remains out of phase-one scope.
