# ConsensusGuard — final technical review

Review date: 2026-10-12. This review covers the full local contract, all three
test files, test compatibility code, CI/toolchain configuration, and project
security documentation. It is not formal verification, a live Studio run, or
an external audit attestation.

## Current finding fixed

`_reach_decision.analyze_sources()` previously called `gl.nondet.exec_prompt`
whenever at least one source body passed integrity checks, unless a retryable
outage was also present. With `min_valid_sources = 2`, one good source plus a
returned 404 could therefore invoke the LLM. If the model failed or returned
malformed JSON, the transaction reverted instead of recording the intended
`INCONCLUSIVE / INSUFFICIENT_HASH_VERIFIED_SOURCES` result. The same defect
affected appeal rounds.

The classifier now runs only if `len(verified_sources) >= min_valid_sources`.
Below the threshold, classification cannot change the result, so the code
leaves the default per-source `UNCLEAR` labels untouched. Deterministic code
then either reverts without state writes if a source is `UNAVAILABLE`, or
appends an agreed `INCONCLUSIVE` result if all insufficient evidence is
otherwise terminal for that round. Direct Mode regressions cover first
resolution, appeal, the no-LLM-call condition, and appeal rollback when
classification is required but malformed.

## Source and function review map

| Code area | Review result |
|---|---|
| Constants, `require`, address and digest helpers | Bounds and lowercase 64-character digest syntax are checked before storage/use. |
| `strict_json_loads`, `_normalize_manifest` | JSON object duplicate keys are rejected in manifests; schema is exact; 2–5 URLs, unique canonical URL/host, and lowercase SHA-256 syntax are enforced. |
| `_canonical_url` | Bounded GenVM-compatible string parser. It rejects direct IP literals, localhost/local suffixes, userinfo, unsafe ports, fragments, controls, malformed/reserved escapes, repeated separators, and dot segments. Host spelling and safe percent escapes are canonicalized. It does not resolve DNS or prove public routing. |
| `_policy_sha256` | Versioned canonical JSON binds `domain`, `claim`, and `criteria` as separate named fields. Legacy newline collisions are regression-tested. |
| `_classification_prompt` | Evidence delimiters are escaped and source text is marked untrusted. This reduces prompt injection but cannot guarantee model robustness. Claim/criteria are requester-controlled inputs. |
| `open_case` | Validates trimmed claim/policy/key, canonical manifest and configured threshold; requester-scoped key is one-use; persists `OPEN` case. |
| `resolve` | Case bound, requester identity, and `OPEN` state checked before external work. One successful round can be appended. |
| `appeal` | Requester only, only after a recorded decision, at most once, and validates a new manifest before running the same decision path. A failed transaction does not consume the appeal. |
| `_reach_decision` and `analyze_sources` | HTTP retrieval, body hash/size/UTF-8 checks, classifier threshold gate, strict label shape/count checks, and validator re-execution. No storage writes occur in the nondeterministic closure. |
| `validator_fn` | Requires a GenVM return and exact canonical observation match. Body/status/label drift is disagreement, not a stored `INCONCLUSIVE`. |
| Decision calculation and writes | Counts verified URL entries; only post-consensus deterministic code derives the outcome, appends an immutable decision, and advances state/latest pointer. |
| Views | Validate IDs; expose canonical case, decision, counts, labels, and append-only history. |

The test fixtures and Direct Mode monkeypatch were separately reviewed. They
adapt the pinned GenLayer Testing Suite's import/storage path and make
cloudpickle round-trip failure fatal for leader/validator closures. They do
not simulate independent Studio validator processes.

The public contract interface uses GenLayer fixed-width `u256` types for
integer arguments and return values. Internal indexing converts these values
to Python integers after validation. The regression
`test_public_integer_schema_uses_fixed_width_genlayer_types` prevents bare
Python `int` from reappearing in public signatures, because it is unsupported
for GenLayer's typed schema interface.

## Decision threshold meaning

Let `m = min_valid_sources`, `v` be hash-matching, non-empty, size-bounded,
UTF-8 bodies, `s` be `SUPPORTS`, and `r` be `REFUTES` among the verified
entries.

| Condition | Contract result |
|---|---|
| `v < m` and any fetch is classified `UNAVAILABLE` | Revert/no state write; requester may retry |
| `v < m` with no `UNAVAILABLE` fetch | `INCONCLUSIVE / INSUFFICIENT_HASH_VERIFIED_SOURCES` |
| `s >= m` and `r == 0` | `VERIFIED / SUPPORT_THRESHOLD_MET` |
| `r >= m` and `s == 0` | `REJECTED / REFUTATION_THRESHOLD_MET` |
| Anything else | `INCONCLUSIVE / CONFLICTING_OR_WEAK_EVIDENCE` |

The threshold is a configured quorum, not a majority. For five valid URL
observations, `m = 2`, two `SUPPORTS`, three `UNCLEAR`, and zero `REFUTES`
intentionally yields `VERIFIED`. With `m = 3`, the same labels yield
`INCONCLUSIVE`. Therefore `VERIFIED` means only that the configured number of
model labels support the claim under the requester's committed criteria with
no refutations. It does not mean most sources support it, the publishers are
independent, or the claim is true. Counts are URL observations on distinct
normalized hostnames, not authenticated publishers.

## Source, DNS, and external-input boundaries

- A SHA-256 match proves fetched bytes equal the digest the requester supplied.
  It does not authenticate the publisher, establish authority, or prove truth.
- Different hostnames, including sibling subdomains, can share one operator,
  publish mirrored bytes, or be controlled by the requester. No publisher
  registry, ownership proof, or publisher-signature scheme exists.
- URL validation is syntax-only. The contract passes the submitted URL to
  `gl.nondet.web.get`; it does not resolve/pin DNS, verify the resolved IP, or
  validate a final redirect destination. DNS rebinding, a hostname resolving
  to a private address, and redirect-to-private destinations are not ruled
  out by this contract. Complete SSRF prevention must not be claimed.
- No local test can establish what network egress controls a live GenVM/Studio
  deployment applies. That runtime boundary was not inspected through a real
  Studio multi-validator execution in this environment.
- HTTP 408/425/429, 5xx, and caught transport/DNS exceptions are treated as
  `UNAVAILABLE` and retryable when below threshold. The contract cannot know
  whether a failure will resolve. Other returned non-2xx statuses become
  `HTTP_ERROR` for that attempt; this is not evidence the response is
  permanent. Some 4xx statuses may later change, but only the one appeal is
  available.
- Prompt injection is mitigated by delimiter escaping, untrusted-evidence
  instructions, and exact validator agreement; it is not eliminated. A
  requester also chooses claim and criteria, so the output is conditional on
  those inputs.

## Consensus, disagreement, replay, and rollback review

- GenLayer documentation describes web requests as independent nondeterministic
  operations by leaders/validators; live pages can vary. ConsensusGuard checks
  exact per-source order, URL, expected/observed hash, integrity status, and
  label. Divergent LLMs or source snapshots can leave the transaction
  undetermined. No real Studio validator disagreement result is claimed.
- A malformed classifier result with sufficient evidence reverts before
  append/state update. A below-threshold classifier is now skipped, so it
  cannot block `INCONCLUSIVE` or retry handling.
- `UNAVAILABLE` below threshold preserves `OPEN` or preserves `DECIDED` with
  `appeal_used == false`. Repeated resolution is impossible after a successful
  initial decision; only one requester appeal can succeed. Existing GLSim
  permanent-dissent tests exercise rollback of simulated state across
  rotations, but this is not live protocol rollback evidence.
- Direct Mode tests cover a different requester, duplicate requester-scoped
  key, invalid case IDs, invalid/duplicate manifests, malformed output,
  validator body/status/label drift, retry, and state after failed calls.
- Contract response-format JSON may arrive already decoded by the SDK. Direct
  Mode's JSON mock decodes structured output before the contract receives it;
  duplicate LLM object-key rejection is therefore not claimed. The contract
  checks resulting output type, exact keys, array size, and allowed labels.

## Test record and execution limits

Latest complete local run, Python 3.12.14, Direct Mode GenVM `v0.6.0-rc9`:

- `pytest -q`: **66 passed, 1 skipped** (63 Direct Mode and 3 GLSim).
- New/focused risk regressions: **12 passed**.
- `compileall`, `pip check`, GenVM AST/semantic check, typecheck, and both
  toolchain bundle hashes: passed.
- Fixed-width public integer schema regression: passed.
- GenVM semantic lint uses the separately pinned compatible `v0.3.0-rc7`
  bundle. Feeding the Direct Mode `v0.6.0-rc9` bundle to the linter is not
  supported by its archive layout; this does not constitute same-version
  semantic validation. The linter emits its `I200` newer-runner notice.
- CI YAML was parsed locally, but GitHub Actions itself was not run.
- CI uses immutable action commit refs verified against upstream tags; the
  GitHub-hosted `ubuntu-24.04` image remains managed and mutable.
- Work Cloud Browser Studio Dev schema check was attempted. The
  `gen_getContractSchemaForCode` call failed before presenting a run form with
  `VM_ERROR: invalid_contract runner malformed` under `GenVM v0.3.0-rc7`. The
  same error reproduced for fresh minimal/current-import/legacy-import
  contracts and a copied `storage.py` sample. The browser logs do not expose a
  full backend stack or release manifest, so this establishes the observed
  failure and a likely schema-runner compatibility issue, not a definitive
  internal root cause. Evidence and exact variants are in
  `evidence/studio-dev-schema-investigation.md`.
- Real Studio multi-validator test was not run: the schema failure occurred
  before a run form was available, and no local Studio endpoint or supported
  container/socket setup was available. Its test and runbook remain in the
  package; it must not be represented as passed.
- Testnet deployment, commit/push, Portal submission, and GEN fee transactions
  were not performed.

The test runner initially was absent from the temporary cache and the first
fetch attempt used a nonexistent release asset name. The official fallback
asset was then retrieved and matched the locked SHA-256. A stale linter cache
was also found truncated; the official `genvm-runners-all.tar.xz` was restored,
validated with `xz -t`, and matched the locked hash. The exact events and
outputs are in `evidence/final-review-attempts.md`.

## Official GenLayer references consulted

- Web access and independent request variability:
  <https://docs.genlayer.com/developers/intelligent-contracts/features/web-access>
- Nondeterministic operation and post-consensus storage boundary:
  <https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism>
- Web data trust, source stability, and provenance guidance:
  <https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/web-data-access>

These references explain the platform model; they do not prove this contract's
live Studio behavior or network destination controls.

## Post-review Studio Dev execution addendum — 2026-10-12

After explicit user authorization, Studio Dev deployed the corrected contract
and ran `open_case` plus `resolve(0)` in Normal (Full Consensus) mode. The
resolution reached Studio `ACCEPTED`, `Reached consensus`, and `FINALIZED`;
read-back returned one `VERIFIED` decision, two matching committed/observed
SHA-256 values, and two `SUPPORTS` labels. A first `open_case` transaction
correctly failed with `USER_ERROR: duplicate source host`; the corrected retry
used two distinct hosts and succeeded. The local five-validator harness remains
skipped. The Studio UI did not show validator identities or numeric quorum.
All current details and exact available hashes/read-back data are in
`evidence/studio-dev-live-validation.md`. The historical “not run” statements
above describe the review snapshot before this addendum and are superseded for
Studio Dev only; public testnet, GitHub Actions, and Portal were not used.


## Final completion update — 2026-10-12

The final full local suite is **67 passed, 1 skipped** (68 collected); details and raw output are in `evidence/final-local-tests.log`. The C1 percent-encoded control URL case is now rejected, with a regression test. Fresh compilation, SDK schema, Pyright, dependency consistency, toolchain hashes, and GenVM AST lint passed (`evidence/final-static-checks.log`). GenVM linter semantic `check` / `typecheck` were attempted but could not download their SDK artifact under this workspace's network policy; those checks remain unverified and are not reported as passes.

Studio Dev Explorer evidence confirms the existing deployment and a finalized accepted Full Consensus resolve with five initial validator slots. The vote map is 3 agree / 2 idle, and execution records include idle errors; do not characterize this as five successful executions. The contract state read-back is `VERIFIED` for the controlled fixture. The transaction Explorer record reports an approximate 0.000097 GEN fee. A prior `open_case` failed with the duplicate-host guard and is recorded as a failure. No public testnet deployment, live appeal, induced real-validator disagreement/rollback, or Portal submission is claimed. GLSim's five-vote disagreement/rollback test is simulation-only.

GitHub repo `maho0638/consensusguard-genlayer` was populated; Quality workflow run 38314656919 completed successfully for commit `4f32baa9eb661f7118bc2ab59d10b61472db4cc1`. See `evidence/github-ci.md`. This section supersedes earlier status in this historical review.
