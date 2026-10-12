# ConsensusGuard — independent review handoff

**Snapshot:** 2026-10-12. This document is for a new ChatGPT reviewer who will
inspect the complete source tree from scratch. Read the contract and tests
directly; this handoff and the audit notes are orientation, not proof.

## Project purpose and status

ConsensusGuard is a GenLayer Intelligent Contract that binds a requester claim
and fixed criteria to exact HTTP response-body SHA-256 commitments. Leader and
validators independently fetch and classify evidence; the validator path must
exact-match the ordered body hashes, integrity states, and labels before
deterministic code stores an outcome. The requester may make one appeal with a
new manifest.

This is an evidence integrity/consistency gate, not a truth oracle. A matching
digest proves only that fetched bytes equal bytes committed by the requester.
Model labels are judgments. Distinct hostnames do not prove distinct
publishers, ownership, or factual independence.

The two findings in the previously supplied audit were fixed: `resolve` is
requester-only; transport outages below threshold revert with no decision and
can be retried; URL validation is strict and canonical. A second source review
was completed and is recorded in `SECURITY_AUDIT.md`. The latest local suite before the final C1 URL hardening had 66 passing tests and one local Studio test skipped; final count is recorded in `evidence/final-local-tests.log`. Studio Dev was deployed and a Normal (Full Consensus) `resolve` transaction reached consensus and finalized. The read-back is `VERIFIED` with two verified fixture bodies and two `SUPPORTS` labels. Explorer records five initial validator slots, an accepted outcome, and a vote map of 3 agree / 2 idle; detailed execution records include idle errors, so do not claim five successful independent executions. Explorer reports an approximate 0.000097 GEN fee. No public testnet deployment or Portal submission is evidenced.

Public method integer schemas now use fixed-width `u256`; internal code
converts bounded IDs to Python `int`. This was a compatibility correction for
GenLayer's typed contract schema and is guarded by
`test_public_integer_schema_uses_fixed_width_genlayer_types`.

Studio Dev schema extraction succeeds for both a minimal contract and the
complete migrated contract. The root cause was an obsolete runner hash format
and SDK API surface; the current executor rejects the old runner ID before
Python starts. The exact compatible runner and SDK are pinned and included in
`vendor/`. See `evidence/studio-dev-schema-investigation.md`. The follow-up
live deployment, transaction receipts/statuses, and read-back are in
`evidence/studio-dev-live-validation.md`.

The second independent audit found a policy-digest ambiguity in the former
newline concatenation of claim and criteria. It is fixed with versioned
canonical JSON whose named fields and escaping preserve field boundaries;
regressions cover newline and NUL-containing legacy collisions. Distinct
hostnames, including sibling subdomains, still cannot prove distinct
publishers. The contract counts URL observations only and makes no publisher
independence claim. It has no publisher registry or signature system.

## File guide

| File | Purpose |
|---|---|
| `contracts/consensus_guard.py` | Complete contract: URL parser/canonicalizer, manifest and digest checks, request authorization, evidence fetch/classification, validator equivalence, thresholds, persistent records, views. |
| `tests/conftest.py` | Compatibility bridge between pinned `genlayer-test` 0.30.0rc2 and the current GenLayer Python SDK imports/storage paths. It also patches Direct Mode nondeterministic calls, enables strict cloudpickle dump/load round trips for leader and validator closures, and captures validator callbacks. Test scaffolding only. |
| `tests/test_consensus_guard.py` | Direct Mode input, URL attack, authorization, retry, evidence, threshold, classifier output, validator drift, appeal and state tests. |
| `tests/test_glsim_consensus.py` | Five-vote agreement test, full-rotation contract dissent/rollback test with compatibility shim, and isolated simulator snapshot test. GLSim is a single-process simulator only. |
| `tests/test_studio_multivalidator.py` | Opt-in local Studio integration test, skipped unless `CONSENSUSGUARD_RUN_STUDIO=1`. |
| `gltest.config.yaml` | Local test configuration; leader-only mode is false. |
| `pyproject.toml` | Project metadata and pytest configuration. |
| `requirements-dev.txt`, `requirements-lock.txt` | Top-level test/linter requirements and exact Python dependency freeze. |
| `toolchain.lock.json`, `scripts/verify_toolchain_bundles.py` | SHA-256 pins for the Direct Mode and lint GenVM archives and a verifier run after those tools download their bundles. |
| `scripts/build_handoff.py` | Rebuilds the handoff ZIP and verifies unique members, complete inventory, member SHA-256 values, and ZIP CRC. |
| `.github/workflows/quality.yml` | Reproducible CI job: Ubuntu 24.04, Python 3.12.14, exact Python lock, pinned test/lint GenVM versions and bundle hash verification. It has not been run on GitHub Actions. |
| `DEPENDENCIES.md` | SDK, GenVM bundle, simulator, and linter identities. |
| `README.md` | Overview, guarantees, API and current state. |
| `ARCHITECTURE.md` | Data flow, separation of nondeterministic/deterministic operations, threshold table. |
| `CONSENSUS.md` | Validator exact-match rule, transient outage semantics, source integrity/truth boundary. |
| `STATE_MACHINE.md` | Caller/state transition table and no-write/retry cases. |
| `THREAT_MODEL.md` | Assets, adversaries, mitigations, and residual trust boundaries. |
| `LIMITATIONS.md` | DNS/origin, model, liveness, appeal, and deployment constraints. |
| `DECISIONS.md` | Design decision history. |
| `SECURITY_AUDIT.md` | Initial audit findings, their disposition, and second review invariants/residual issues. |
| `SECOND_REVIEW.md` | Standalone post-fix source review and remaining external verification gate. |
| `FINAL_TECHNICAL_REVIEW.md` | Full-function review, attack-scenario decisions, threshold interpretation, DNS/SSRF limits, and final test evidence. |
| `TESTING.md` | Reproduction commands and honest current test status. |
| `STUDIO_MULTIVALIDATOR_RUNBOOK.md` | Steps to run independent local Studio validators later. |
| `REVIEWER_GUIDE.md` | Manual review and behavioral checks. |
| `PORTAL_SUBMISSION_DRAFT.md` | Draft only; not submitted. |
| `DEPLOYMENTS.md` | Deployment evidence/status across localnet, Studio Dev, and public testnets. |
| `evidence/` | Latest test/static-analysis outputs, earlier blocked/failed attempts, environment diagnostics, and cache/toolchain version boundaries. |
| `evidence/studio-dev-schema-investigation.md` | Corrected root-cause analysis and browser proof that full contract schema loads. |
| `evidence/studio-dev-live-validation.md` | Studio Dev deployment, failed and successful `open_case` attempts, finalized Full Consensus `resolve`, read-back JSON, and evidence limits. |
| `evidence/remediation-notes.md` | Failed early attempts, causes, and fixes retained for review. |
| `ZIP_CONTENTS.txt` | Archive member listing. |
| `SHA256SUMS.txt` | Member checksums (self-excluded). |

Generated `.venv/`, `.tool-home/`, `.pytest_cache/`, `__pycache__/`, and
`artifacts/` are excluded. Secrets and `.env` are excluded.

## Consensus and state flow

1. `open_case` validates case key/claim/criteria, source count and threshold,
   canonicalizes URLs, requires unique canonical URLs and normalized hostnames,
   hashes the canonical manifest, and stores immutable inputs with requester
   address and `OPEN` state.
2. Only that requester can call `resolve`. Each participant fetches the
   committed URLs inside `gl.vm.run_nondet`.
3. A body is integrity `VERIFIED` only if it is HTTP 2xx, non-empty bytes, no
   more than 6,000 bytes, exact SHA-256 match, and valid UTF-8. It then becomes
   a classifier input. This says nothing about origin authenticity or truth.
4. The classifier emits one `SUPPORTS`, `REFUTES`, or `UNCLEAR` label for each
   eligible URL only when at least `min_valid_sources` entries pass integrity
   checks. Each validator repeats requests and classification and exact
   compares canonical JSON observations.
5. HTTP 408/425/429, 5xx, and transport/DNS exceptions are classified as
   `UNAVAILABLE`. If fewer than `min_valid_sources` bodies pass integrity
   checks and any URL is `UNAVAILABLE`, the call reverts with no state write;
   the requester can retry. This is a retry policy, not proof that a failure
   is temporary. A failed appeal remains `DECIDED` and does not consume the
   one appeal.
6. Other returned non-2xx codes are `HTTP_ERROR` for this attempt; they are
   not proven permanent. If the threshold is not met, accepted consensus
   stores `INCONCLUSIVE`. Digest/size/encoding problems below threshold and
   conflict/weak labels also store `INCONCLUSIVE`.
7. If accepted, deterministic code appends `DecisionRecord`, updates latest
   pointer, and moves `OPEN -> DECIDED`. One requester-only appeal appends a
   second record and moves `DECIDED -> APPEALED`.
8. Protocol-level validator disagreement is a consensus/transaction status,
   not an `INCONCLUSIVE` contract result. It should not append a decision; the
   live Studio rollback behavior remains untested here.

### Threshold table

Let `m = min_valid_sources`, `v` be matching UTF-8 bodies, `s` be supporting
labels, and `r` be refuting labels.

| Condition | Result |
|---|---|
| `v < m` and any source is `UNAVAILABLE` | Revert; preserve current state for retry |
| `v < m` and no source is `UNAVAILABLE` | `INCONCLUSIVE / INSUFFICIENT_HASH_VERIFIED_SOURCES` |
| `s >= m` and `r == 0` | `VERIFIED / SUPPORT_THRESHOLD_MET` |
| `r >= m` and `s == 0` | `REJECTED / REFUTATION_THRESHOLD_MET` |
| Any other label mix | `INCONCLUSIVE / CONFLICTING_OR_WEAK_EVIDENCE` |

`VERIFIED` is a decision outcome based on model labels and integer URL
thresholds. The per-source integrity label `VERIFIED` means bytes matched the
requester digest. Neither is an authenticity or truth proof. Distinct hosts are
not authenticated independent publishers.

The threshold is a configured quorum, not a majority. With five
hash-verified URL observations and `m = 2`, two `SUPPORTS`, three `UNCLEAR`,
and zero `REFUTES` deliberately produce `VERIFIED`; with `m = 3`, that exact
label set produces `INCONCLUSIVE`. Consumers must read the counts and
`reason_code` to interpret the outcome.

`min_valid_sources` and result counters count hash-verified URL entries on
distinct normalized hostnames. Two sibling subdomains may share one operator
and are not cryptographically independent publishers. This implementation
offers no publisher identity or ownership attestation.

`policy_sha256` is SHA-256 of canonical JSON with `domain`, `claim`, and
`criteria` named separately; the domain is `ConsensusGuard.Policy.v1`. Earlier
newline-concatenated digests are not rewritten. This workspace has no deployed
state, so no migration was needed. A deployment with historical decisions
would need an explicit version policy before interpreting this field.

## URL rules and residual risk

The contract uses bounded GenVM-compatible string parsing, no `urllib` import.
It accepts only lowercase `https://`, ASCII DNS hostnames, and default HTTPS
port. It canonicalizes host casing/trailing dot, removes `:443`, decodes
percent-encoded unreserved bytes, and inserts `/` for an empty path. It rejects
IP literals (including direct IPv4/IPv6 forms), localhost/local suffixes,
single-label hosts, userinfo, non-default ports, fragments, whitespace/control
characters, non-ASCII, backslashes, malformed/control or reserved percent
escapes, repeated path separators, and dot-segment paths. It allows one URL per
canonical hostname. It cannot prove that two URLs with different paths on
different hosts return semantically different resources.

This is URL syntax validation, not proof of public DNS/routability. The
contract does not resolve/pin DNS, inspect resolved IPs, or validate a final
redirect destination. DNS rebinding, private destinations behind public-looking
hostnames, and redirect-to-private destinations are not ruled out. Different
domains/subdomains may share control. GenVM runtime egress protections were not
verified in a real Studio environment.

## Audit changes and regression coverage

- Previously permissionless `resolve` could let a third party consume a case
  with an agreed outage-induced `INCONCLUSIVE`. Now only requester can resolve;
  unavailability below threshold causes a no-write retry revert.
- `appeal` has the same retry behavior and does not set `appeal_used` on a
  failed transient attempt.
- URL validation now blocks the reported address/authority/controls/canonical
  aliases and rejects multiple paths on one canonical host.
- Provenance documents distinguish byte hash, host diversity, and truth.
- Added attacks/regressions verify non-requester resolution, transient first
  resolution and appeal retry, direct private/local addresses, userinfo,
  controls, fragments, unsafe path/port, canonical alias collisions, unique
  hostname policy, and stored canonical spelling.
- Current review found and fixed a gate bug: if fewer than `min_valid_sources`
  bodies passed integrity, `analyze_sources` could still call the LLM when the
  below-threshold gap consisted of an HTTP response rather than a retryable
  `UNAVAILABLE`. Classifier errors could then block the intended
  `INCONCLUSIVE`. Initial resolution and appeal regressions verify no LLM call,
  the stored result, and correct state transitions.
- Five-source threshold regression confirms `m=2`, 2 `SUPPORTS`, 3 `UNCLEAR`,
  0 `REFUTES` => `VERIFIED`; with `m=3`, the same labels => `INCONCLUSIVE`.
  This is the documented configured quorum, not a majority vote.
- GLSim forced-dissent investigation: the earlier failed probe injected dissent
  for only two of three rotations, then stopped; the third rotation finalized.
  A new test keeps every validator dissenting in every rotation and checks
  `UNDETERMINED`, `OPEN`, and zero decisions after rollback. This verifies only
  GLSim's own snapshot path, not Studio or GenLayer production consensus.

## Exact local evidence

Python 3.12.14; pinned project dependencies. Latest expected output is recorded
in `evidence/`:

- `python -m compileall -q contracts tests` — pass.
- `pytest -q` — **66 passed, 1 skipped**: 63 Direct Mode tests plus 3 GLSim
  checks pass; the opt-in Studio test is skipped. The suite includes the
  original 33 passing tests before added regressions.
- `genvm-lint lint contracts/consensus_guard.py --json` — pass, 3 AST checks.
- `scripts/check_contract_sdk.py` — pass, schema extracted by the exact pinned
  SDK (8 public methods).
- Pyright — run against the same pinned SDK source with dynamic-storage
  suppressions in `pyrightconfig.json`; see `evidence/current-typecheck.json`.
- `pip check` — pass.
- Toolchain verifier — runner and SDK ZIP SHA-256 values match
  `toolchain.lock.json`. Direct Mode, GLSim, schema extraction, and Pyright use
  the same SDK identity as Studio Dev. The installed linter's semantic loader
  is obsolete (`genlayer.py` import); only its AST lint is counted as passed.
- Strict cloudpickle dump/load round trips for both nondeterministic closures
  are enforced; the targeted check passed, as did the full suite.
- Studio Dev live test — deployed and executed in Normal (Full Consensus)
  mode. The Studio interface recorded `Reached consensus` and `FINALIZED` for
  `resolve(0)`, and state reads returned one case and one `VERIFIED` decision.
  The fixture is synthetic, designed to exercise byte hashes and classification;
  it says nothing about the truth of a real world claim or publisher
  independence. The interface did not expose validator identities/count, so
  this handoff claims consensus status but not a numeric participant quorum.
  The first `open_case` attempt failed with the expected duplicate-host
  rejection; the corrected retry is documented and succeeded.
- Local five-validator Studio harness — remains skipped. It is a separate
  localnet test; follow `STUDIO_MULTIVALIDATOR_RUNBOOK.md` when a local GenLayer
  Studio network is available.
- GitHub Actions, public testnet, and Portal — outcomes are separately recorded in the final status addendum. No public testnet or Portal action is evidenced.

An initial typecheck attempt failed because `pyright` was not on `PATH`; the
successful rerun set `PATH` to the project venv. Earlier no-network SDK/test
attempts and the failed/incomplete GLSim probe remain documented rather than
being hidden. The latest complete command output is authoritative.

## How to independently review and reproduce

1. Read this handoff, then inspect `SECURITY_AUDIT.md`, the full contract,
   tests, and docs. Recompute behavior; do not trust this summary alone.
2. Install Python 3.12+, then `python -m pip install -r requirements-lock.txt`.
3. Run `python scripts/verify_toolchain_bundles.py`,
   `python scripts/check_contract_sdk.py`,
   `pyright -p pyrightconfig.json --outputjson`, and `pytest -q`.
4. Run `genvm-lint lint contracts/consensus_guard.py --json`.
5. To reproduce the separate local five-validator harness, follow
   `STUDIO_MULTIVALIDATOR_RUNBOOK.md` on a machine with local GenLayer Studio
   and Docker. Preserve receipts, node/validator logs, and full output.
6. Keep the Studio Dev evidence, localnet test, public testnet, CI, deployment
   and Portal outcomes separate. Do not label a skipped/unrun check as passed.

The installed GenVM linter's semantic loader is incompatible with the current
SDK import layout; this was directly observed as `No module named genlayer.py`.
The handoff uses the pinned SDK's own schema extractor and Pyright against its
vendored source instead. Older evidence files preserve prior attempts, while
the corrected current result and root cause are in
`evidence/studio-dev-schema-investigation.md`.

## Current completion addendum — 2026-10-12

The initial local review count above is historical. A new C1-percent-encoded URL control rejection was added with a targeted negative test; the complete final run and updated handoff ZIP are authoritative. The Studio Dev deployment and transaction are described in `evidence/studio-dev-live-validation.md`; the explorer data shows five validator slots but only 3 agree and 2 idle votes, with execution caveats. The approximate Explorer fee for the resolve transaction is 0.000097 GEN. This is not public testnet evidence. The local Studio harness is not equivalent to Studio Dev transaction consensus.

For the latest GitHub branch/commit, Actions result, and final package hashes, inspect `evidence/final-status.md`, `evidence/github-ci.log`, `SHA256SUMS.txt`, and `evidence/archive-integrity.txt`. Portal submission remains intentionally unperformed. No mainnet funds or transaction were used.
