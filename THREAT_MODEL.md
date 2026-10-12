# Threat model

## Assets

- The committed claim, criteria, source manifest, and digests.
- The integrity and provenance trail for each accepted decision.
- Correct case ownership, decision thresholds, and appeal history.
- Safe behavior when sources or validators disagree.

## Adversaries

- A requester who supplies misleading sources, dishonest criteria, duplicate URLs, or a false expected digest.
- A webpage author who changes a source after a case is opened or embeds prompt-injection instructions.
- A leader that fabricates labels or ignores source evidence.
- A resolver who attempts replay, unauthorized appeal, or duplicate decision writes.
- A source host, DNS path, or HTTP service that is unavailable or returns different bytes to validators.

## Controls

| Threat | Control |
|---|---|
| Evidence changed after commitment | Hash exact HTTP response bytes and require a match to the precommitted digest. |
| Leader invents a decision | Every validator independently fetches, hashes, and classifies every verified source; all ordered labels and observations must match. |
| Source failure or hash mismatch misrepresented as support | The source is not passed to the classifier and receives a non-verified integrity status. |
| Weak or contradictory evidence forced into a binary verdict | Separate `INCONCLUSIVE` branches and explicit no-mixed-evidence decisive conditions. |
| Malformed or oversized inputs | Strict bounds on case key, claim, criteria, manifest size, source count, response bytes, URL scheme, and digest syntax. |
| Duplicate/aliased URL or same-host path counted twice / key replay | Canonical URL aliases and duplicate normalized hostnames are rejected; case keys are unique per requester; cases transition once. |
| Third party consumes a case or a retryable outage finalizes it | Only the requester may resolve; below-threshold `UNAVAILABLE` observations revert without a decision and preserve retry state. This status is a retry policy and does not prove the underlying fault is temporary. |
| Unauthorized or repeated appeal | Only the original requester can appeal once; decisions are append-only. |
| Prompt injection in evidence | Evidence delimiters are escaped and labeled untrusted in the prompt; per-source labels must also match across validators. This reduces prompt injection risk but does not make the LLM immune to adversarial content. |
| DNS rebinding, a hostname resolving to a private IP, or redirecting to a private destination | Not prevented by contract URL syntax validation. The contract does not perform DNS resolution/IP pinning or inspect the final redirect destination. Use trusted URLs; do not treat this as complete SSRF protection. |

## Explicit trust limits

- HTTPS plus a digest does not prove that a source is truthful or that its domain is the correct authority. The requester commits the digest; it is not an attestation by the publisher.
- Distinct hostnames are not proof of independent ownership or editorial independence. A publisher can mirror content across several domains or subdomains.
- `min_valid_sources` and result counters count hash-verified URL entries on distinct normalized hostnames. They must not be interpreted as a count of independent publishers or independent factual corroboration. Sibling subdomains remain possible and are not ownership-authenticated.
- The contract does not authenticate an off-chain publisher signature or establish legal facts.
- LLMs can still make correlated errors. Exact agreement is a consistency gate, not a truth guarantee.
- Different LLM outputs or source snapshots can cause validator disagreement and an undetermined/reverted transaction. The contract performs exact observation-and-label matching; it does not prove validators use independent model providers or eliminate correlated model errors. This behavior has not been tested with independent Studio validator processes here.
- The requester controls claim and criteria. A decision means the committed evidence was classified under those submitted criteria; it does not certify that the question or criteria are neutral, complete, or suitable for downstream use.
- URL checks validate a narrow string form only. DNS and redirects are outside the contract's observable boundary; whether the deployment environment adds network egress protections was not verified in this local test environment.
- A changed response, changing source, unavailable host, provider behavior, or validator disagreement can keep a case unresolved. That is a liveness limitation, not a stored negative decision.
- The contract is not an escrow and moves no funds. It must not be used as sole authorization for irreversible value transfer without a separate application-level policy.
