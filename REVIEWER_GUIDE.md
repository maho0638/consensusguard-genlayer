# Reviewer guide

## 1. Confirm inputs and ownership

Deploy `contracts/consensus_guard.py`. Call `open_case` with a unique key, a factual claim, fixed criteria, a JSON manifest of 2–5 canonical HTTPS URLs on distinct hostnames, exact lowercase SHA-256 digests of response body bytes, and `min_valid_sources` in the range 2 through the source count. Read `get_case(0)` and confirm its state is `OPEN` and its manifest digest is fixed. Distinct hosts do not prove distinct publishers.

## 2. Resolve a matching case

Use stable, small UTF-8 endpoints. Call `resolve(case_id)`. Inspect `get_latest_decision(case_id)` and verify every verified source's observed digest equals the committed digest. Repeat the read and check the decision's policy digest, manifest digest, exact per-source labels, outcome, and counts.

## 3. Exercise fail-safe behavior

- Change a source body after committing its digest: it must be marked `MISMATCH` and excluded from classification.
- Return HTTP 503/429/408: the source observation is `UNAVAILABLE`; if fewer than the required source threshold is met, `resolve` must revert and leave the case `OPEN` for the requester to retry. A returned permanent status such as 404 is `HTTP_ERROR` and may produce `INCONCLUSIVE`, allowing a corrected appeal.
- Supply source labels that mix `SUPPORTS` and `REFUTES`: the accepted contract-level result must be `INCONCLUSIVE`.
- Make leader and validator labels differ: consensus must fail to accept the decision write; do not call that an `INCONCLUSIVE` record.

## 4. Exercise replay and appeal

Try a second `resolve` after a decision and a second `appeal` after an appeal; both must revert. Try an appeal from another address; it must revert. The first decision remains available at `get_decision(0)` after a successful appeal.

## 5. Interpret the result correctly

The verdict is a consensus-backed classification under requester-supplied criteria. The requester-supplied hashes pin the evidence bytes but do not authenticate the publisher or prove the claim true. Check `LIMITATIONS.md` before using the result for external value or irreversible actions.
