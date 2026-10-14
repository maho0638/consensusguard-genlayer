# ConsensusGuard — Phase 6 final regression, security and real Studio audit
Date: 2026-10-14

**Verdict: PHASE 6 PASS — all defined technical gates passed.**
This report is not a claim of formal verification, zero future vulnerabilities,
production-readiness, or approval to submit to the Portal. Final delivery ZIP
and release gate are phase 7, NOT performed here.

## A. Exact independent test and CI evidence

| Control | Verified result | Proof |
|---|---|---|
| Full Python Direct Mode + adversarial inputs | **98 PASS, 3 Studio opt-in SKIP, zero fail** | https://github.com/maho0638/consensusguard-genlayer/actions/runs/38555562772 |
| Python 3.12 compileall | PASS | Same Quality CI |
| Current GenVM AST/semantic linter | PASS, 0 errors | Same Quality CI |
| Official contract-SDK/API compatibility script | PASS | Same Quality CI |
| Pinned vendored toolchain integrity script | PASS | Same Quality CI |
| Pyright contract types | PASS, no error diagnostic | Same Quality CI |
| Dependency consistency (pip check) | PASS, no broken requirements | Same Quality CI |
| Pinned dependency vulnerability advisory audit | **67 packages scanned; 0 known advisories** | https://github.com/maho0638/consensusguard-genlayer/actions/runs/38555288470 |
| Exact real local Studio integration | **3 PASS, 0 FAIL** | https://github.com/maho0638/consensusguard-genlayer/actions/runs/38555170256 |
| All local Studio transaction finalization | **12 FINALIZED; 0 unfinished; 0 blocked** | [Sanitized full Studio audit](audit-studio-phase6-full-38555170256.md) |
| Worker lifecycle | **12 finalization starts, 12 completions, 0 errors** | Same Studio audit |
| Historical Studio Dev two idle validators (phase 5, not replayed here) | PASS, direct read-only receipt check | https://github.com/maho0638/consensusguard-genlayer/actions/runs/38553677412 |

The three Studio integration tests were deliberately **skipped in offline pytest**
and instead run for real in the independent fully provisioned Studio v0.123.0-rc.7
Docker/network CI. Therefore '3 skipped' is **not** silently claimed as
normal pytest PASS; real CI https://github.com/maho0638/consensusguard-genlayer/actions/runs/38555170256 proves all three.

## B. On-chain local Studio coverage (same CI run)

- Deploy + open + resolve + appeal: **3 agree, 2 idle**, each idle explicitly
  `CONSENSUS_VALIDATOR_QUORUM_REACHED`, `fatal=false`; old decision VERIFIED,
  new appeal decision REJECTED; immutable previous evidence commitment retained.
- Disagreement with no spare validator: **0 agree, 3 disagree, 2 idle** in one
  realization, explicit `Undetermined` round, `rotation_count=0`,
  `OPEN`, decision_count=0, unchanged committed case; deterministic recovery
  `DECIDED`, one VERIFIED decision.
- Five-validator committee with one spare sixth validator: **2 agree,
  3 disagree**, `Leader Rotation → Undetermined`, `rotation_count=1`,
  unchanged `OPEN` case and zero decisions; then healthy retry stores exactly
  one VERIFIED decision.
- All 12 transactions in one isolated Studio stack finalized; use the
  **on-chain contract readbacks + consensus history** to interpret outcome:
  the top-level FINALIZED transaction lifecycle does not mean a rejected
  proposed state was committed.
- Transaction IDs and safe vote/worker diagnostics are preserved in
  [audit-studio-phase6-full-38555170256.md](audit-studio-phase6-full-38555170256.md).
- These are **real local Studio** transactions with deterministic mock
  HTTP/LLM transport, **not** new Studio Dev/Bradbury live-user transaction
  proof or source-publisher authenticity proof.

## C. Security review and newly added regression tests

The source audit rechecked permission boundaries: only the requester may
resolve or appeal, a case cannot be resolved twice, one appeal is append-only,
and transaction failure/disagreement cannot mutate committed decisions.
Manifest and prompt integrity controls include strictly bounded HTTPS URL
canonicalization, distinct normalized hosts, committed per-source SHA-256,
invalid/missing source data handling, classifier schema validation, and
independent validator revalidation.

Phase-six expansion adds 30 extra passing offline test cases over the
previous 68, including percent-encoded control/reserved URL smuggling,
private/local hostname variants, overlong/ambiguous JSON manifests,
duplicate key overwrite attempts, wrong-case canonicalization, multi-user
case-key isolation, and malformed/typed/duplicated JSON LLM classifications.
All check rejection or data isolation against the actual Direct Mode
contract, not a reimplemented parser.

**Concrete security issue remediated:** the older source-bundle GitHub workflow
used the mutable tag `actions/upload-artifact@v4`; phase six pinned it to
the verified official immutable tag commit
`ea165f8d65b6e75b540449e92b4886f43607fa02` (GitHub
`actions/upload-artifact` `refs/tags/v4`).
Other inspected repository Actions already used pinned SHA references.
The historical source-bundle workflow still intentionally references the
**old production commit** for its legacy archive; phase 7 must build the
new single ZIP from the new audited revision. That old workflow was not run
as phase six.

Third-party dependency check uses the locked
`requirements-lock.txt`. The additional vulnerability scan (pip-audit,
`--no-deps --disable-pip`) returned exit=0 with 67 dependency entries
and zero known vulnerability advisories. This is **not** a guarantee against
undisclosed future vulnerabilities or malicious dependencies.

## D. Source integrity, version discipline, and release restrictions

- Production contract `contracts/consensus_guard.py` is **unchanged**
  from the phase-five verified audit source, Git blob
  `ca4df13afea4accc90e858aab5f71cb420242c57`.
- The previous audited Studio tests also retain their respective blob SHA:
  `test_studio_multivalidator.py` `e1c790a126e7c64568705b51cc8974094c7f49f9`;
  `test_studio_phase4_disagreement.py` `87730c952124b602fa47ca39e628b0c8e402103f`;
  `test_studio_phase4_rotation.py` `7cae76a800be97ee3735bcc0a3dca4955cc9acdf`.
- Pinned `requirements-lock.txt` unchanged, blob
  `171b55e860d855503d6580c1c655c53a96401b1d`.
- Studio tests run against official pinned GenLayer Studio
  `v0.123.0-rc.7`, local fully simulated chain id 61127.
- No merge, push to `main`, Vercel deployment, Portal resubmission,
  production wallet signature, or GEN token spend.
- The branch is **audit/phase6-full-security-regression-20261014**.

## E. Remaining honest limits

- Distinct DNS hostnames do NOT cryptographically authenticate independent
  publishers, ownership, or factual truth; public-looking DNS may rebind or
  redirect toward private IP destinations unless restricted by the external
  network/GenVM layer. This is documented in `THREAT_MODEL.md` and
  `CONSENSUS.md`, and was not silently labeled fixed.
- Model classification and prompt-injection resistance are not formal
  guarantees; repeated independent classifier execution reduces but cannot
  eliminate semantic uncertainty.
- The tests use deterministic mocked evidence in a real local
  five-validator Studio environment. They are not mainnet tests or a
  new execution of the historical Studio Dev contract.
- Historical Studio Dev idles were independently resolved in phase five using
  the original 2026-10-12 transaction receipt, not by assuming local mock
  behavior represents historical facts.
- No external formal penetration test, third-party audit, complete DNS
  security guarantee, or proof of all future network runtime states is claimed.

**Phase 6: COMPLETE / PASS for the tested technical scope.**
**Phase 7 (latest source + all proof in a single SHA-256 checked ZIP, final
release decision) remains NOT STARTED.**
