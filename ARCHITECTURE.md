# Architecture

## Purpose

ConsensusGuard is a reusable content-addressed evidence adjudication primitive. Its job is to preserve the exact decision inputs and make the leader prove its interpretation against independently repeated evidence retrieval and classification.

## Data flow

1. A requester opens a case with a unique requester-scoped key, a claim, fixed criteria, source URLs, expected SHA-256 response-body digests, and a minimum source threshold.
2. The deterministic path validates and canonicalizes the manifest, records the requester and timestamp, and stores the fixed policy and manifest.
3. Only the requester can submit `resolve(case_id)`. Each consensus participant independently fetches the same source URLs inside a non-deterministic block.
4. The source body is hashed before decoding. Only HTTP 2xx, non-empty, UTF-8 bodies at or below the size bound whose digest exactly matches the committed digest are sent to the classifier.
5. The leader classifies each verified source separately. Each validator repeats the fetch and classification. The custom validator accepts only an exact match of ordered source observations and labels.
6. If fewer than the requested threshold are hash-verified, the LLM classifier is skipped. If any fetch is classified `UNAVAILABLE`, the call reverts without a state write and the requester may retry while the case remains `OPEN`; this is a retry policy, not proof the failure is temporary. Without an `UNAVAILABLE` observation, accepted consensus stores `INCONCLUSIVE`. Otherwise, deterministic code counts verified, supporting, refuting, and unclear URLs; derives one outcome; and appends a decision record.
7. The requester can submit one appeal using a new manifest. The appeal decision is appended; the first decision is not overwritten.

## Separation of concerns

- **Non-deterministic work:** web retrieval and semantic classification only.
- **Consensus check:** exact JSON equality of each source's expected and observed hash, integrity state, and classification label. Free-form explanation text is not stored or compared.
- **Deterministic work:** input limits, digest checks, threshold calculations, authorization, replay protection, timestamps, and storage writes.
- **Persistent state:** one `DynArray[CaseRecord]`, one append-only `DynArray[DecisionRecord]`, and a `TreeMap` preventing requester-scoped key reuse.

The contract performs one classifier call per leader or validator execution only when at least `min_valid_sources` entries pass byte, size, and encoding checks. The call covers all eligible entries in a fixed order. Insufficient evidence cannot become more sufficient through classification, so no classifier call is needed below that threshold. The model cannot change a case's claim, criteria, source manifest, result thresholds, or caller permissions.

## Decision function

Let `m` be `min_valid_sources`; let `v`, `s`, and `r` be the counts of hash-verified, supporting, and refuting sources.

| Condition | Outcome | Reason |
|---|---|---|
| `v < m` with any `UNAVAILABLE` URL | Revert; remain `OPEN` | Retry later |
| `v < m` without an `UNAVAILABLE` URL | `INCONCLUSIVE` | `INSUFFICIENT_HASH_VERIFIED_SOURCES` |
| `s >= m` and `r == 0` | `VERIFIED` | `SUPPORT_THRESHOLD_MET` |
| `r >= m` and `s == 0` | `REJECTED` | `REFUTATION_THRESHOLD_MET` |
| otherwise | `INCONCLUSIVE` | `CONFLICTING_OR_WEAK_EVIDENCE` |

Thresholds use integer URL counts; there is no floating-point score or fuzzy boundary. `min_valid_sources` is both the minimum number of hash-verified entries required before classification and the minimum number of direct `SUPPORTS` or `REFUTES` labels required for a decisive outcome. This is a configured quorum, not a majority of all verified URLs. For five verified entries with `m = 2`, two `SUPPORTS`, zero `REFUTES`, and three `UNCLEAR` produce `VERIFIED`; with `m = 3`, the same labels produce `INCONCLUSIVE`. `VERIFIED` means the configured support quorum was met under the supplied criteria; it does not mean most sources agreed or that the claim is objectively true. Different hostnames are required, but publisher ownership is not verified, so URL counts must not be described as independent publishers or independent truth corroboration. Mixed support and refutation cannot satisfy either decisive branch.

`policy_sha256` uses SHA-256 over canonical JSON for the named fields
`domain`, `claim`, and `criteria`, with `domain` fixed to
`ConsensusGuard.Policy.v1`. JSON escaping and explicit field names bind the
policy fields without delimiter ambiguity. This replaces the earlier newline
concatenation encoding; historical records retain their old digest and are not
rewritten. No deployed state is part of this local project snapshot.

`min_valid_sources`, `verified_count`, and the support/refute counters are
counts of distinct normalized-host URL entries that pass body-integrity checks
and model labels. They do not count authenticated publishers. Sibling domains
may have one operator; the contract has no ownership registry, publisher
signature scheme, or other mechanism to establish publisher independence.

## Why this differs from Penumbra

Penumbra explores a broad catalog of 20 consensus primitives, including uncertainty oracles and multi-source corroboration. ConsensusGuard is a single-purpose evidence-integrity gate: it binds every evaluation to caller-committed raw-response digests, performs exact per-source classification comparison across leader and validators, and exposes a one-time append-only appeal round. It is not a renamed oracle: the source-byte commitment and exact evidence-to-decision audit trail are the core contract invariant.
