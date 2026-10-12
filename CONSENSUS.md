# Consensus design

## Equivalence rule

`gl.vm.run_nondet(leader_fn, validator_fn)` is used because the outcome depends on non-deterministic HTTP responses and LLM classification. `strict_eq` over a live web response would be too brittle, while `prompt_comparative` could accept semantically similar answers with different source sets or labels.

The validator independently re-runs the same operation for each manifest entry, independently hashes the returned body, and independently classifies the verified evidence. It accepts only when the canonical JSON for all observations is byte-identical to the leader's canonical JSON. Specifically, each entry must agree on:

- source position and committed URL;
- expected SHA-256 digest;
- observed SHA-256 digest, or empty digest if retrieval failed;
- integrity status (`VERIFIED`, `MISMATCH`, `UNAVAILABLE`, `HTTP_ERROR`, `INVALID_SIZE`, or `INVALID_ENCODING`);
- label (`SUPPORTS`, `REFUTES`, or `UNCLEAR`).

The validator does not check only output shape or a score range. It repeats source retrieval and interpretation, so it verifies the decision substance against the same evidence and fixed criteria.

## Transaction behavior

The contract writes nothing from inside the non-deterministic block. Only after `run_nondet` returns an accepted result does deterministic code derive the final outcome and append the decision. If validators disagree, GenLayer consensus may leave the transaction undetermined; no `INCONCLUSIVE` decision is stored. Classification is skipped whenever fewer than the evidence threshold are hash-verified. If any URL is `UNAVAILABLE` (transport/DNS exception, HTTP 408/425/429, or 5xx), the requester-only resolution reverts without writing state and may be retried. The contract cannot know whether a network failure will actually be temporary. Other returned non-2xx statuses are `HTTP_ERROR` for this attempt; if the threshold is not met, the agreed result is `INCONCLUSIVE` and the requester can appeal with a corrected manifest. This response-code policy does not establish that those errors are permanent. Available responses that fail commitment/size/encoding checks are also terminal `INCONCLUSIVE` for that round.

## Prompt-injection boundary

Retrieved page text is enclosed as untrusted evidence. The prompt says to ignore embedded instructions and classify only under the immutable criteria. This reduces prompt-injection risk but cannot prove that a model is immune to adversarial text. Repeated independent classification and exact outcome agreement provide the contract's decision gate; they do not turn an LLM judgment into objective truth.

## Source integrity, origin, and truth

The digest proves equality between response bytes and the requester's committed digest. `VERIFIED` integrity means only that byte equality plus size and UTF-8 checks passed. The classifier's `SUPPORTS` label is a model judgment. Distinct canonical hostnames avoid counting multiple paths on a single host, but they do not prove different ownership, editorial control, origin, or factual truth. The contract has no trusted publisher registry or publisher signature scheme. The submitted URL is syntax-checked before `gl.nondet.web.get`; the contract does not resolve or pin DNS, validate the resolved IP, or validate a final redirect destination. DNS rebinding and redirect-to-private-destination protections are therefore not guaranteed by this contract. Do not use untrusted URLs or treat this validation as complete SSRF protection.

## Cost and liveness

For `n` sources, each leader and validator performs up to `n` requests and one classifier call. Each call is bounded to at most five sources and 6,000 response bytes per source. Dynamic or unavailable sources can prevent validator agreement. Retries may be needed, but repeated failure is not translated into a stored result without consensus.

Counts are over URL entries on distinct normalized hostnames; they are not
publisher-independence counts. Sibling subdomains can share an operator, and
the contract does not authenticate publisher identity. Validator agreement
means consistent retrieval and classification by consensus participants, not
independent source ownership or truth.

For `m = 2`, two support labels and three unclear labels among five verified
URLs intentionally meet the configured support quorum. The outcome is not a
majority vote; consumers must interpret `VERIFIED` as “at least m classifier
labels support under the committed criteria, with zero refutations.”

The decision `policy_sha256` is SHA-256 of canonical JSON with the explicit
fields `domain = "ConsensusGuard.Policy.v1"`, `claim`, and `criteria`. This
structured encoding prevents different policy pairs from aliasing through a
shared delimiter.
