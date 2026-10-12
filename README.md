# ConsensusGuard

**An evidence-bound decision primitive for GenLayer Intelligent Contracts.**

ConsensusGuard records a claim, fixed evaluation criteria, a bounded evidence manifest, and the SHA-256 digest expected for each HTTPS response. When a case is resolved, the leader and each validator independently fetch the evidence, verify its committed digest, and classify each verified source as `SUPPORTS`, `REFUTES`, or `UNCLEAR`. The contract compares the complete ordered source observations and labels exactly before it writes a decision.

This is a reusable decision gate, not an “AI truth” oracle. A content hash proves that fetched bytes match a digest committed by the requester; it does not prove that the source is authentic, authoritative, independent, or true. Different hostnames also do not prove different owners or publishers.

## Why GenLayer

A conventional deterministic contract cannot decide whether evidence semantically supports a natural-language claim. ConsensusGuard puts that judgment in a non-deterministic operation and uses GenLayer's leader/validator execution to check it. All authorization, thresholds, hashes, state transitions, and writes remain deterministic.

## Core guarantees

- The requester commits the claim, criteria, source URLs, expected SHA-256 digests, and evidence threshold when opening a case.
- The criteria and initial manifest are immutable after opening.
- The leader and validators independently fetch the same committed sources and independently classify each hash-verified source.
- Validators must match the leader on each source's observed digest, integrity status, and exact label. A mismatch fails consensus; it does not become `INCONCLUSIVE`.
- The LLM is called only after at least `min_valid_sources` entries pass the body-integrity checks. Below that count, any `UNAVAILABLE` response causes a no-write revert for retry; otherwise consensus can store `INCONCLUSIVE` without depending on an unnecessary LLM call. `UNAVAILABLE` is a retry policy classification, not a finding that a failure is temporary.
- A successful decision is appended to an immutable decision history. A requester may submit one appeal with a new manifest; the earlier decision stays queryable.
- Only the requester may resolve or appeal. Replays, duplicate requester-scoped case keys, invalid manifests, malformed model output, and unauthorized calls revert before recording state.

## Repository map

- [`contracts/consensus_guard.py`](contracts/consensus_guard.py) — standalone GenVM contract.
- [`tests/test_consensus_guard.py`](tests/test_consensus_guard.py) — direct-mode logic, boundary, replay, and validator checks.
- [`tests/test_glsim_consensus.py`](tests/test_glsim_consensus.py) — five-vote GLSim simulation (single-process, not Studio).
- [`tests/test_studio_multivalidator.py`](tests/test_studio_multivalidator.py) — opt-in five-validator Studio integration test.
- [`ARCHITECTURE.md`](ARCHITECTURE.md), [`CONSENSUS.md`](CONSENSUS.md), [`STATE_MACHINE.md`](STATE_MACHINE.md), [`THREAT_MODEL.md`](THREAT_MODEL.md) — design and security boundaries.
- [`TESTING.md`](TESTING.md), [`STUDIO_MULTIVALIDATOR_RUNBOOK.md`](STUDIO_MULTIVALIDATOR_RUNBOOK.md), and [`REVIEWER_GUIDE.md`](REVIEWER_GUIDE.md) — how to reproduce and review.
- [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md), [`SECOND_REVIEW.md`](SECOND_REVIEW.md), [`FINAL_TECHNICAL_REVIEW.md`](FINAL_TECHNICAL_REVIEW.md), [`DEPENDENCIES.md`](DEPENDENCIES.md), and [`HANDOFF_TO_CHATGPT.md`](HANDOFF_TO_CHATGPT.md) — audit history, full current review, toolchain versions, and independent-review handoff.
- [`LIMITATIONS.md`](LIMITATIONS.md) and [`DEPLOYMENTS.md`](DEPLOYMENTS.md) — explicit limits and deployment evidence.

## Local checks

Use Python 3.12.14, then install the pinned test framework:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m compileall -q contracts tests
genvm-lint check contracts/consensus_guard.py --json
genvm-lint typecheck contracts/consensus_guard.py --json
pytest -q
```

`gltest` direct mode can exercise mocked web and LLM outcomes without network access. CI verifies the checked-in runner and SDK ZIP hashes and uses that same SDK for Direct Mode, GLSim, and schema extraction. Pyright checks the contract against the vendored pinned SDK types. Direct Mode tests also require cloudpickle round trips for both nondeterministic closures. Studio Dev schema and a Normal (Full Consensus) transaction have been exercised; a separate local five-validator harness remains a separate opt-in test.

Public integer parameters and return values use fixed-width `u256` types;
bare Python `int` is not used in the GenLayer-facing schema. Studio Dev schema generation succeeds with the migrated runner and SDK. The root cause and browser evidence are recorded in [`evidence/studio-dev-schema-investigation.md`](evidence/studio-dev-schema-investigation.md). Studio Dev live deployment and transaction results are documented in [`evidence/studio-dev-live-validation.md`](evidence/studio-dev-live-validation.md).

## Contract API

1. `open_case(case_key, claim, criteria, manifest_json, min_valid_sources)` — commit a case and its evidence manifest.
2. `resolve(case_id)` — requester-only; compare validator evidence and append the first decision, or revert for retry when a below-threshold fetch is classified `UNAVAILABLE`.
3. `appeal(case_id, new_manifest_json)` — requester-only, one-time re-review with new evidence commitments.
4. `get_case`, `get_decision`, and `get_latest_decision` — read the state and append-only audit trail.

Manifest format:

```json
[
  {"url":"https://evidence.example/record.json","sha256":"<64 lowercase hex characters>"},
  {"url":"https://archive.example/record.json","sha256":"<64 lowercase hex characters>"}
]
```

The hash is SHA-256 of the exact HTTP response body bytes, before UTF-8 decoding. Sources must be stable and small (up to 6,000 bytes each). The contract requires 2–5 canonicalized HTTPS URLs with distinct normalized hostnames and at least 2 matching sources for any decisive result. This is URL-level diversity only; ownership and editorial independence are not verified.

The `min_valid_sources` threshold counts distinct normalized-host URL entries,
not independently authenticated publishers. Different subdomains can belong
to one publisher and may repeat the same material; no publisher identity or
independence proof is implemented. The same threshold is the support/refute
quorum, not a majority rule. For `m = 2`, two `SUPPORTS` and three `UNCLEAR`
among five verified entries intentionally produce `VERIFIED`; this means the
configured support quorum was met under the committed criteria, not that most
sources agreed or that the claim is true.

URL validation is syntax-only. The contract does not resolve/pin DNS, inspect
resolved IPs, or validate redirect destinations. DNS rebinding, hostnames
pointing to private IPs, and redirect-to-private destinations are not ruled
out; this contract must not be treated as complete SSRF protection.

`policy_sha256` is SHA-256 over canonical JSON containing the version domain
`ConsensusGuard.Policy.v1` and separately named `claim` and `criteria` fields.
This field-bounded encoding avoids delimiter collisions. Existing historical
decision records, if any, retain their original digest; this workspace has no
deployed state to migrate.

## Project status

The repository was empty when the work began. The current handoff includes a verified Studio Dev deployment and finalized Full Consensus transaction. Explorer records five initial validators, an accepted consensus result, and `FINALIZED`; its vote map lists three `agree` and two `idle` votes. Contract read-back returned one `VERIFIED` decision with two matching source digests and two `SUPPORTS` labels. The Explorer fee is approximately `0.000097 GEN`; the Studio wallet UI rounded its displayed balance to `0 GEN`. These are Studio Dev records, not a public testnet deployment. No Portal submission has been made.

See `evidence/studio-dev-live-validation.md` for transaction identifiers and the precise limits of the validator evidence. The local opt-in network integration remains skipped because this workspace has no local GenLayer node; the live Studio Dev transaction is separately evidenced and must not be conflated with that skipped local test. CI action commits, Python packages, and GenVM bundles are pinned; the hosted Ubuntu 24.04 runner image remains managed and mutable.
