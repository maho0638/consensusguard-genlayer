# Second source review — post-fix

Date: 2026-10-12. This is the post-fix review pass after applying the supplied
independent audit findings. It is a fresh review of the modified contract,
tests, and state machine, with targeted regression tests and GenVM static checks.
It is not a cryptographic proof, live Studio review, or external auditor
attestation.

## Third review pass — second independent audit findings

The prior `claim + "\\n" + criteria` policy digest was ambiguous. It has been
replaced by SHA-256 of canonical JSON with explicit `domain`, `claim`, and
`criteria` fields, using domain/version `ConsensusGuard.Policy.v1`. JSON
escaping plus named fields bind both values unambiguously. Regression tests
exercise two distinct pairs that collide under the former concatenation,
including NUL-containing values, and verify the exact canonical digest.

Subdomain ownership is not observable from the contract's URL parser. The
contract still requires distinct normalized hostnames and permits sibling
subdomains because public-suffix heuristics would not prove common or separate
ownership and can be wrong for delegated/tenant domains. Result thresholds and
counters are therefore documented as URL-entry observations, never as
independent publishers or factual corroboration. No registry/signature
identity feature is claimed. A test pins that the example sibling-host
manifest is accepted only as two URL observations, not an independence proof.

Historical decisions created with the previous digest encoding are immutable
and are not rewritten. This local snapshot has no deployed state. Any later
deployment that needs to consume old and new decisions must distinguish the
digest version explicitly at the application boundary.

## Findings checked

| Area | Review result | Evidence / boundary |
|---|---|---|
| Resolution authorization | Pass | `resolve` checks case bounds, requester identity, then `OPEN` state before evidence work; Direct Mode rejects another address and leaves state open. |
| Temporary outage and retry | Pass | If fewer than the configured threshold are hash-verified and any source is `UNAVAILABLE`, classifier work is skipped and a revert occurs before append/state writes. Tests cover initial resolution and appeal retry. |
| Decision thresholds | Pass | Integer conditions implement support/refute threshold with no contrary labels; unavailable below threshold is retryable; content-integrity failure without transport unavailability can become `INCONCLUSIVE`. Decision table tests cover boundaries. |
| Manifest and canonical URL | Pass for specified parser rules | Rejects local/IP literals, userinfo, unsafe ports, fragments, control/non-ASCII/backslash, malformed/control/reserved percent escapes, repeated separators and dot segments; normalizes case, default port, trailing dot, unreserved escapes; rejects URL aliases and a second URL on same host. Attack tests cover these rules. |
| DNS rebinding/private destinations behind a hostname | Residual | The contract does not resolve/pin DNS or use an allowlisted publisher registry. A public-looking hostname may still resolve to a private destination. This risk must remain explicit. |
| Evidence provenance and truth | Residual by design | Digest equality proves bytes match the requester's own commitment; hostname diversity, including sibling subdomains, does not prove ownership or publisher independence; LLM labels do not prove truth. Counters are documented as URL-entry observations. |
| Validator agreement | Pass in Direct Mode | Existing disagreement tests cover body/status/label drift. GLSim agreement and permanent disagreement/rollback simulator tests pass. Neither proves real independent Studio validators. |
| State transitions and appeal | Pass in Direct Mode | First successful resolution appends once and moves to `DECIDED`; one successful requester appeal appends and moves to `APPEALED`; outage rollback preserves `OPEN` or unused appeal. |
| GenVM code compatibility | Pass to tested static boundary | `genvm-lint check` (AST + semantic) and `genvm-lint typecheck` pass. This does not prove deployed behavior. |

## No additional contract-code issue found

I did not find an additional deterministic contract defect in authorization,
write ordering, threshold calculation, evidence digest handling, retry state,
or append-only decision history in this pass. The residual DNS/private-destination
limitation and publisher-authentication gap mean the project must not claim
complete SSRF prevention, independent origin verification, or truth assurance.

In the third review pass, I inspected the new policy encoder for field
separation and version-domain binding, checked its regression coverage against
newline and NUL collision examples, and verified that source-count language
does not imply publisher independence. The suite at that time had 58 passing tests
and one opt-in Studio test skipped. The repeatable CI configuration now pins
Python dependencies and the Direct Mode/GLSim GenVM bundle independently, and
verifies both bundle hashes. Strict cloudpickle round trips are also enforced
for nondeterministic closures. The semantic linter still requires its separate
`v0.3.0-rc7` bundle; the failed attempt to use the `v0.6.0-rc9` test runner as
the linter bundle is preserved as a known toolchain-format limitation. Updated
checks and evidence are included with the handoff.

## Required next external verification

Run `CONSENSUSGUARD_RUN_STUDIO=1 gltest tests/test_studio_multivalidator.py
-v -s --network localnet` on a machine with supported local GenLayer Studio.
Preserve full output, transaction receipt, and validator logs. Do not substitute
the single-process GLSim test for this result.

## Latest full technical review

The subsequent review found one additional deterministic logic defect: with
fewer than `min_valid_sources` verified bodies, a returned HTTP response (for
example 404) plus one valid body still triggered the LLM. The LLM was not
needed to decide `INCONCLUSIVE`, but malformed/model failure could revert
instead. The same path existed on appeal. `analyze_sources` now classifies
only after the configured number of bodies pass integrity checks. New
initial-resolution and appeal tests verify the classifier is not called and
the expected decision/state is stored. A separate appeal test verifies
malformed classifier output with enough evidence leaves the prior decision
and unused appeal unchanged.

The threshold was confirmed as an explicit configured quorum rather than a
majority: with five verified URLs and `m=2`, 2 `SUPPORTS`, 3 `UNCLEAR`, and no
`REFUTES` intentionally yields `VERIFIED`; at `m=3`, it is `INCONCLUSIVE`.
Docs and boundary tests explain this meaning.

The URL parser's “public DNS name” wording was narrowed because syntax-only
validation cannot establish public routability. DNS rebinding, private DNS
answers, and redirect-to-private destinations remain unblocked by contract
code. Documentation does not claim complete SSRF protection. Manifest JSON
duplicate keys are now rejected to avoid last-key-wins ambiguity.

At the time of this review the complete suite was **65 passed, 1 skipped**: 62 Direct Mode and 3
GLSim; the Studio integration remains unrun. `FINAL_TECHNICAL_REVIEW.md`
records the function-by-function and attack-scenario review. Current command
outputs and verified toolchain artifacts are included in `evidence/`.
