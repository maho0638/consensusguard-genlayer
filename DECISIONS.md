# Design decisions

## D1 — Bind decisions to source bytes, not only URLs

URLs are mutable pointers. A requester must commit each expected SHA-256 digest at case opening. Resolution hashes the exact HTTP response bytes before UTF-8 decoding and sends only exact matches to the classifier.

## D2 — Re-fetch and re-classify on every validator

A shape-only validator would trust the leader's substance. Each validator repeats source retrieval and classification, then exact-compares ordered observations and labels. Any mismatch prevents the application-level write.

## D3 — Use exact labels and integer source counts

Numeric confidence scores introduce threshold-edge ambiguity and invite overclaiming. The contract stores only categorical per-source labels and derives outcomes with integer thresholds. A `SUPPORTS` label is still a model judgment, not a cryptographic proof.

## D4 — Keep disagreement separate from an inconclusive decision

`INCONCLUSIVE` is an ordinary recorded decision only if consensus accepts the same evidence observations and counts. Validator disagreement leaves the transaction without a decision. A caller cannot treat protocol-level undetermined status as a contract-level outcome.

## D5 — Append appeals instead of overwriting

The requester gets one re-review with a new committed manifest. The first decision remains readable so downstream consumers can inspect the full history and round that produced the latest result.

## D6 — One contract, no value transfers

This project is a reusable decision primitive. It carries no funds and does not embed an app or frontend. Applications can use its read API as one input to their own deterministic policy.

## D7 — Runner and test framework pin

The contract magic comment pins the documented `py-genlayer` runner hash used by the current GenLayer examples. `genlayer-test` is pinned to the latest published 0.30.0 release candidate available during research (0.30.0rc2, 2026-09-03), because the current official migration guidance identifies the v0.6 / Studio-dev toolchain as a compatible release-candidate family. This repository does not claim the RC against an untested stable network; CI must install the pinned release and run Direct Mode.

## D8 — Versioned, field-bounded policy digest

The policy digest hashes canonical JSON with the named `domain`, `claim`, and `criteria` fields, where the domain is `ConsensusGuard.Policy.v1`. A delimiter join is unsafe because the input fields may contain that delimiter. Historical digests are immutable; this local implementation has no deployed records to migrate.

## D9 — URL diversity does not claim publisher independence

The manifest requires distinct normalized hostnames to prevent duplicate URLs or multiple paths on one host from trivially multiplying a threshold. The contract has no reliable proof of publisher ownership: sibling subdomains may share an operator, and domain suffix heuristics do not establish control. Counts are therefore URL-entry observations only. Authenticated publisher identity would require a separately designed trust registry or signatures.
