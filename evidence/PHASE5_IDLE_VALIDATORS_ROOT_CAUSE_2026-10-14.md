# ConsensusGuard Phase 5 — Two IDLE validators: verified cause and historical boundary

Date: 2026-10-14. This report concerns ONLY phase 5. **Local Studio root cause VERIFIED. Historical Studio Dev error cause NOT independently verified.**

## Verified execution
- Version: GenLayer Studio `v0.123.0-rc.7`; isolated GitHub Actions Docker stack, Python 3.12, five separate Studio validator records with deterministic mock HTTP/LLM responses.
- Studio integration CI (SUCCESS, zero failed steps): https://github.com/maho0638/consensusguard-genlayer/actions/runs/38532431448
- Quality CI (SUCCESS): https://github.com/maho0638/consensusguard-genlayer/actions/runs/38532431429
- Machine-generated sanitized transaction and worker evidence (PASS): [audit-studio-phase5-idle-38532431448.md](audit-studio-phase5-idle-38532431448.md)
- Audit branch: `audit/studio-phase5-idle-validator-20261014`. No production contract change, no main merge, public submission, wallet signature, Studio Dev transaction, or test GEN expenditure.

| Stage | Local Studio transaction | Observed votes | Every IDLE's checked diagnostic |
|---|---|---|---|
| Deploy | `0x905769672b3a35ebb11e2eff766d418206f0cb173bbb6c4e22c37214e25c8768` | — | FINALIZED |
| Open case | `0xbf3aad1c532255ea128a57367e25930fd641599d0e5bf841e30d6b64018fcfe9` | — | OPEN |
| Resolve | `0x2e71f9b9e810f46b3e32b152e078b366d27320d69967e6daf17dd6fcec17a985` | 3 agree + 2 idle | exactly two `CONSENSUS_VALIDATOR_QUORUM_REACHED` |
| Appeal | `0xaedbca41bea2ba55386083ea1664736f4e9b30b147d804f65ade8cf3197cc374` | 3 agree + 2 idle | exactly two `CONSENSUS_VALIDATOR_QUORUM_REACHED` |

The checked `genvm_result.raw_error` cause for **all four** idle receipts is `VALIDATOR_QUORUM_REACHED` and `fatal = false`. Every idle vote was matched to exactly one independent validator receipt (across `consensus_data.validators` and `leader_receipt[1:]`), with five distinct addresses registered. Zero unexplained idle receipts, zero failed worker tasks, and four completed finalizations. Final case is `APPEALED`: original immutable decision `VERIFIED`, new decision `REJECTED`, `decision_count = 2`.

## Source-level root cause (pinned Studio release)
In `genlayerlabs/genlayer-studio` release `v0.123.0-rc.7`, `backend/consensus/base.py`, the committing state runs validator executions concurrently, computes whether the remaining pending votes could change the majority, cancels pending asyncio tasks once quorum is mathematically locked, and produces synthetic `Vote.IDLE` receipts with `CONSENSUS_VALIDATOR_QUORUM_REACHED`, `VALIDATOR_QUORUM_REACHED` and `fatal: False`. These are **cancelled unfinished executions**, not two independent negative votes, not evidence that all five validators agreed, and not necessarily infrastructure faults. See: https://github.com/genlayerlabs/genlayer-studio/blob/v0.123.0-rc.7/backend/consensus/base.py and https://github.com/genlayerlabs/genlayer-studio/blob/v0.123.0-rc.7/backend/consensus/utils.py.

Expected local behavior is a 3-of-5 quorum with two deliberately cancelled validator slots. Contract reads and receipt causes, not `FINALIZED` alone, are decisive. The phase-5 opt-in regression is `tests/test_studio_multivalidator.py` with `CONSENSUSGUARD_PHASE5_IDLE_PROOF=1`. Do not treat cancellation as a contract bug or remove consensus validators merely to make every vote appear as agree.

## Historical Studio Dev event — evidence limit
The separate Studio Dev write on **2026-10-12** is `0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9` on contract `0xBa84783D71d902c8BD3Ba63418Df172280249139`. The archived browser-derived record `evidence/studio-dev-live-validation.md` confirms Full Consensus, five validator slots, a three-agree/two-idle vote map, two recorded idle execution errors, and a persisted `VERIFIED` decision. However it **does not preserve the two idle receipts' exact `genvm_result.error_code`, `raw_error.causes`, or `fatal` fields**. The public transaction-detail endpoint could not be accessed for independent read-back from this environment. Consequently the older Studio Dev idles may be the same cancellation mechanism but **that historical causal attribution remains unproven**. This is not repaired by rerunning a new *local* test or by citing an upstream source alone.

To resolve the historical question without a new write, obtain the existing Studio Dev transaction's full consensus JSON and inspect the two idle receipts for both standard error tokens and `fatal=false`; if either differs, investigate its actual error rather than relabeling it as benign. No new Studio Dev wallet transaction is necessary.

**Verdict:** Phase-five local technical regression and explicit mechanism **PASS**. Retrospective Studio Dev attribution is separately **UNVERIFIED due missing archival diagnostic data**. Evidence is not manufactured and the scope is not silently widened.
