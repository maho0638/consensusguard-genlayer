# Testing and run status

## Test layers

1. Python syntax compilation for contract, tests and tooling.
2. GenLayer Direct Mode tests using the SDK archive whose runner matches the Studio Dev schema runner.
3. Validator callback re-execution with agreeing and dissenting observations.
4. GLSim five-vote simulation in a single local process.
5. Studio Dev browser schema extraction and a deployed Full Consensus transaction (evidenced separately).
6. Local five-validator integration remains opt-in and needs a running local GenLayer node. Public testnet deployment and Portal submission are not evidenced.

The suite covers thresholds and boundaries, malformed inputs/model output, content hash/size/encoding failures, unauthorized resolve/appeal calls, transient outage retries for initial resolution and appeals, URL/IP/userinfo/control/alias cases, state transitions, validator drift, and read bounds.

## Reproduce locally

```bash
python -m pip install -r requirements-lock.txt
python scripts/verify_toolchain_bundles.py
python -m compileall -q contracts tests scripts
python scripts/check_contract_sdk.py
pyright -p pyrightconfig.json --outputjson
pytest -q
python -m pip check
```

`vendor/runners` holds the exact runner and standard-library SDK ZIPs used by Studio Dev. Their SHA-256 values, manager release and source commit are in `toolchain.lock.json`. `tests/conftest.py` points Direct Mode at this pinned runner tree and requires cloudpickle dump/load round trips for both nondeterministic closures.

`genvm-lint lint` runs its AST checks successfully. The installed `genvm-lint check` semantic loader still imports the obsolete `genlayer.py` module path and therefore cannot validate the migrated SDK; `scripts/check_contract_sdk.py` uses the pinned SDK's own schema generator instead. `pyrightconfig.json` contains the small SDK-specific suppressions needed for the dynamic storage annotations; inspect it before relying on the typecheck result.

## Latest results

On 2026-10-12, local Direct Mode and GLSim tests: **67 passed, 1 skipped** (68 collected; the new C1 percent-encoded control URL attack regression is included). The skipped test is the opt-in local Studio five-validator integration test. Studio Dev schema checks passed for a minimal contract and the complete contract. A live Studio Dev transaction was also deployed and executed in Normal (Full Consensus) mode; it reached consensus, finalized, and read back one `VERIFIED` decision with two matching source hashes and `SUPPORTS` labels. The fixture uses deterministic Base64 response endpoints and does not prove source independence or claim truth. Full transaction and state evidence is in `evidence/studio-dev-live-validation.md`.

The Studio Dev Full Consensus transaction is `FINALIZED`; Explorer records five initial validator slots, an accepted result, and a vote map of 3 `agree` and 2 `idle`. Detailed validator execution records include idle errors; see the evidence caveat. This is a real Studio Dev transaction, distinct from the skipped local integration harness.


GitHub Actions Quality run 38314656919 on commit `4f32baa9eb661f7118bc2ab59d10b61472db4cc1` completed successfully, including pinned dependency install, `pip check`, runner/SDK checksum validation, compileall, AST lint, exact SDK schema extraction, Pyright, and pytest. The GenVM-linter semantic `check`/`typecheck` was separately attempted in this workspace but its SDK artifact download was denied by network policy; it is not counted as passed. Exact outputs and boundaries are in `evidence/`.
