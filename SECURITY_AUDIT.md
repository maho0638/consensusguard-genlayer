# Independent source and logic audit

Review date: 2026-10-12. This document records the original independent report,
the fixes made against its findings, and a second source review after the fixes.
Scope: full contract source, all tests, test compatibility shim, configuration,
CI, and technical documents. This is not a formal verification or live-chain
audit.

## Second-review conclusion

The two reported code defects are fixed and regression-tested: resolution is
requester-only; transient source outages below the evidence threshold preserve
the case and are retryable; and manifest URLs are strictly parsed and
canonicalized in bounded GenVM-compatible string code. The second review also
checked all state writes, thresholds, manifest/decision digests, authorization,
retry behavior, and validator observation comparison. No additional
deterministic contract defect was identified in those paths.

Remaining material limitations: distinct hostnames do not establish distinct
owners, publishers, or truth; DNS names can still resolve to private addresses
and the contract cannot pin DNS; GenLayer Studio multi-validator rollback has
not been tested here. GLSim disagreement/rollback is now covered by a
permanent-dissent contract test using a storage-descriptor compatibility
adapter, plus an isolated simulator snapshot test. The earlier incomplete
probe remains recorded as failed. See `LIMITATIONS.md`, `THREAT_MODEL.md`, and
`evidence/exploratory-dissent-probe.md`.

## Independent report findings and disposition

### 1. Permissionless `resolve` and outage finalization — fixed

Before the fix, anyone could call `resolve`; an agreed observation containing
an HTTP/DNS failure could produce a terminal `INCONCLUSIVE` and move the case
to `DECIDED`. The contract now requires the original requester for both
`resolve` and `appeal`. If fewer than `min_valid_sources` bodies have a matching
hash and any source is transiently `UNAVAILABLE` (transport error, HTTP
408/425/429, or 5xx), resolution reverts before classification or storage
writes. The case remains `OPEN`; a failed appeal remains `DECIDED`
with `appeal_used == false`. The requester can retry. Direct-mode regression
tests cover third-party resolution, first-resolution retry, and appeal retry.

Other returned non-2xx statuses are recorded as `HTTP_ERROR`; if the threshold
is not met, the agreed `INCONCLUSIVE` remains terminal and the requester can
use the one appeal with a corrected manifest. If the configured threshold is
already met, an additional unavailable URL does not block a result: the
declared threshold governs. A permanently silent required URL can still block
liveness until it recovers.

### 2. URL parsing and canonical forms — fixed with an explicit boundary

Manifest URLs are limited to lowercase `https://` with an ASCII DNS hostname.
The validator rejects empty/single-label/local hostnames, IPv4/IPv6 literals,
local-only suffixes, userinfo, non-default ports, fragments, controls,
non-ASCII characters, backslashes, malformed/control percent escapes, and
`.`/`..` path segments, repeated path separators, and percent-encoded reserved
bytes. Host case and trailing dot are normalized; explicit port 443 is removed;
percent-encoded unreserved characters are decoded. Canonical duplicate URLs
and multiple entries on one normalized host are rejected. The input parser
uses no `urllib` or network package so it remains usable in GenVM.

This blocks direct private-IP and localhost URL spellings, but cannot guarantee
that a public-looking DNS name will not resolve or later rebind to a private
address. The contract SDK exposes no DNS pinning/allowlist control in this
implementation. Treat this as a residual SSRF/network trust limitation; use
trusted, immutable public evidence hosts.

### 3. Source provenance versus hash equality — corrected in design/docs

`VERIFIED` integrity is strictly a byte-integrity label: the fetched body is
non-empty, within the size cap, valid UTF-8, and equals the requester's
precommitted SHA-256 digest. `SUPPORTS`/`REFUTES` are model classifications.
Neither proves publisher identity, authority, independence, or truth. The
manifest now permits only one URL per normalized hostname, but hostnames can
share an owner, use mirrors, or publish the same material. Threshold counts
URLs/hosts, not authenticated independent publishers. A trusted source registry
or publisher signatures would be needed for stronger origin claims.

## Second-review invariants checked

- **Input and manifest:** JSON object shape is exact; count is 2–5; minimum is
  between 2 and the manifest size; digest syntax is lowercase 64-hex; canonical
  URL and hostname uniqueness is enforced before case storage; URL digest
  commitment is computed over the canonical manifest.
- **Request authorization:** case IDs are bounded before access; only the
  requester resolves and appeals; requester-scoped keys cannot be reused;
  case state and one-appeal gates are checked before work.
- **Evidence handling:** exact response bytes are hashed before decoding;
  transport/408/425/429/5xx failures are `UNAVAILABLE`, other non-2xx are
  `HTTP_ERROR`; empty, oversized,
  non-byte, mismatched, or invalid-UTF-8 bodies are not classifier inputs.
- **Validator check:** leader and validator repeat ordered fetch/classification
  and compare canonical JSON including index, URL, expected/observed digest,
  integrity, and label. Disagreement is not converted into a stored decision.
- **Thresholds:** with `m = min_valid_sources`, `v` matching UTF-8 bodies, `s`
  support labels, and `r` refute labels: `v < m` plus any `UNAVAILABLE` reverts;
  `v < m` with no temporary outage is `INCONCLUSIVE`; `s >= m, r == 0` is
  `VERIFIED`; `r >= m, s == 0` is `REJECTED`; all other mixes are
  `INCONCLUSIVE`.
- **Storage boundary:** case/decision writes occur outside the nondeterministic
  block and only after it returns. Retry reverts do not append a decision or
  consume the appeal. Decisions are append-only; appeal updates only the latest
  pointer/state.
- **Untrusted text:** source URL/text are escaped and evidence text is marked
  untrusted in the classifier prompt. This reduces prompt-injection risk but
  does not prove model robustness.

## Test and static-check evidence

The latest recorded run is **66 passed, 1 skipped**: 63 Direct Mode cases and
three GLSim tests passed; the Studio integration is skipped by
default because no local Studio node is available. GenVM lint, semantic
validation, compileall, typecheck, and dependency consistency are separately
recorded under `evidence/`. The previous 33 passing tests were preserved and
the new tests cover the reported authorization, transient retry, URL,
canonicalization, policy-field separation, and source-independence boundary.

The original GLSim forced-dissent probe is not a passing test; its follow-up
identified that it only forced two of three rotations. The corrected tests
keep dissent active across every rotation and pass with the compatibility
adapter. This proves only local GLSim behavior; real Studio validator-process
behavior remains unverified. Read `TESTING.md` and
`evidence/exploratory-dissent-probe.md` for exact boundaries.

## Latest full-source review — insufficient-evidence classifier call [fixed]

The review found that the leader invoked the classifier with any verified
source, even when fewer than the configured minimum were available. That
unnecessary call could make a deterministic `INCONCLUSIVE` result or retry
revert if the LLM failed. The classifier is now gated on the full evidence
threshold. First-resolution and appeal regressions prove that malformed mocked
LLM output is not consulted below threshold; a sufficient-evidence appeal
regression confirms that a required classifier failure still reverts without
consuming the appeal or writing a decision. The final complete run is
**66 passed, 1 skipped**; detailed function-by-function findings are in
`FINAL_TECHNICAL_REVIEW.md`.

## Second independent audit findings and remediation

### Finding A — ambiguous policy digest [fixed]

The previous encoding hashed `claim + "\\n" + criteria`, allowing different
field pairs containing newlines to produce identical preimage bytes. This was
an encoding ambiguity, not a SHA-256 cryptographic collision. The contract now
hashes canonical JSON containing separately named `claim` and `criteria`
fields and the explicit domain/version `ConsensusGuard.Policy.v1`. JSON
escaping preserves the field boundaries for newline, NUL, and Unicode values.
Regression tests create distinct claim/criteria pairs that collide under the
old concatenation, including a NUL-containing example, then compare the stored
digest with the canonical JSON expected value.

Changing this encoding changes `policy_sha256` for records created under the
old implementation. Decision history is append-only, so old digests must not
be rewritten. This local package has no deployed chain state. Any future
consumer that spans versions must track the digest version at its application
boundary; the `ConsensusGuard.Policy.v1` domain identifies new-format values.

### Finding B — sibling hostnames do not prove publisher independence [design boundary]

The parser enforces unique normalized hostnames, not unique operators or
publishers. `alpha.publisher.example` and `beta.publisher.example` may be
controlled by one publisher. A registrable-domain heuristic is not reliable
proof of ownership, and hostname strings do not establish legal or operational
control. The implementation therefore makes no independent-source claim:
`min_valid_sources` and result counters count URL entries on distinct
normalized hostnames. The security guarantee is limited to requester-committed
response-byte hashes, model classifications, and validator agreement on those
observations. Authentic publisher identity would require a separately
designed trust registry or publisher signatures, neither of which exists.

The regression test confirms sibling subdomains can appear as separate URL
observations. This is intentional and is not a test of independent ownership.

## Studio Dev schema compatibility follow-up — corrected

Public method integer schemas use fixed-width `u256`; regression tests reject
bare Python `int` annotations. The earlier conclusion that Studio's schema
service was failing is superseded. A current runner + SDK migration made both
a minimal contract and the complete contract schema load in Studio Dev. Source
inspection of the current executor and direct browser logs identify the cause:
the old runner hash was not valid GVM32 and was rejected before Python startup;
the contract also used removed SDK import/decorator/nondeterministic APIs.
The exact SDK/runner identities and browser observation are recorded in
`evidence/studio-dev-schema-investigation.md`. The subsequent Studio Dev
deployment and Full Consensus transaction are recorded in
`evidence/studio-dev-live-validation.md`; the UI recorded consensus and
finalization but did not expose validator identities or numeric quorum.
