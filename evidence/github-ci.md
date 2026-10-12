# GitHub Actions CI evidence

- Repository: `https://github.com/maho0638/consensusguard-genlayer`
- Workflow: `Quality` (`.github/workflows/quality.yml`)
- Run: `38314656919` — `https://github.com/maho0638/consensusguard-genlayer/actions/runs/38314656919`
- Trigger: push to `main`
- Commit: `4f32baa9eb661f7118bc2ab59d10b61472db4cc1`
- Job `direct-tests` (`115028294473`): **completed / success**.

GitHub Actions job-step metadata returned success for each of: setup, checkout, Python setup, `pip install -r requirements-lock.txt`, `pip check`, runner/SDK bundle SHA verification, compileall, GenVM AST lint (3 checks), pinned SDK schema extraction, Pyright, and pytest. Job-step metadata is the evidence preserved here; anonymous GitHub web UI did not expose raw streamed console logs. The complete workflow run is publicly inspectable at the URL above.

The CI job runs pytest with the pinned local runner/SDK bundles. The separate opt-in Studio integration test remains skipped unless a local GenLayer Studio node is configured. CI success is not a public testnet deployment or Portal review.

## Follow-up on the final documentation commit

- Run: `38314886697` — `https://github.com/maho0638/consensusguard-genlayer/actions/runs/38314886697`
- Commit: `e229385bd7676719fec5766788b57bd12ddcb89c`
- Job `direct-tests` (`115029037392`): **completed / success**.
- All 11 substantive workflow steps completed with `success`, including pinned install, checksums, compilation, lint, SDK schema, Pyright, and pytest.

This follow-up run verifies the commit containing the final user-facing status and test-evidence updates. The full source commit was independently green in run `38314656919` as well. Job-step outcomes were retrieved from GitHub Actions metadata; no raw console stream was exposed by the connected public repository view.
