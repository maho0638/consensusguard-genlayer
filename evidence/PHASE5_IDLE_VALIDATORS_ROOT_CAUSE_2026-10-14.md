# ConsensusGuard Phase 5 — Two IDLE validators: verified cause and historical boundary

Date: 2026-10-14. This report concerns ONLY phase 5. **Both local Studio AND historical Studio Dev idle causes are now VERIFIED from the corresponding execution receipts.**

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

## Historical Studio Dev event — independently verified (read-only)

On **2026-10-12**, the historic Studio Dev full-consensus `resolve` transaction
`0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9`
ran on deployed contract `0xBa84783D71d902c8BD3Ba63418Df172280249139`.
The historical browser record `evidence/studio-dev-live-validation.md` showed five eligible validators,
three agree and two idle, but did not archive their exact error-cause fields.
That previous evidence limitation is **resolved**, not merely inferred from a local replay.

An isolated GitHub-hosted **read-only** probe successfully retrieved the original historic
transaction's complete consensus data directly from:
1. Canonical Studio Dev JSON-RPC `eth_getTransactionByHash` — same historic transaction, agree=3, idle=2, matching idle receipts=2, proven quorum cancellation=2, unmatched=0.
2. Studio Dev explorer `/api/transactions/{hash}` — same result.
3. Studio Dev explorer `/api/rpc` proxy with `eth_getTransactionByHash` — same result.

For **both original Studio Dev idle entries**, independently matched to their receipts
using their validator address (not by assuming receipt positions), the probe verified:
- `genvm_result.error_code == "CONSENSUS_VALIDATOR_QUORUM_REACHED"`
- `genvm_result.raw_error.causes` includes `"VALIDATOR_QUORUM_REACHED"`
- `genvm_result.raw_error.fatal is False`
- Vote counts: **3 agree, 2 idle; zero unexplained idle entries.**

The alternate `gen_getTransactionReceipt` method returned JSON-RPC `-32601`
(method unavailable on this RPC); this did **not** block access to the full
historic receipt using `eth_getTransactionByHash`. Results do not reveal
validator identities, private keys, raw transaction data or wallet secrets.

Proof of direct historic retrieval:
- CI SUCCESS: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38553677412
- Sanitized read-only evidence: [historical-studio-dev-idle-readonly-38553677412.md](historical-studio-dev-idle-readonly-38553677412.md)
- Probe source: [historical read-only CI workflow](../.github/workflows/studio-dev-historical-idle-readonly.yml).

This work submitted **no wallet transaction, deployment, faucet request, test-token spend,
contract upgrade, Portal submission or external GitHub issue**. The contract is unmodified.

## Final verdict

**PHASE 5: FULL PASS (local Studio + historical Studio Dev).**
Both historic idle validators were confirmed as **nonfatal early-quorum task cancellations**,
not actual infrastructure failures. The root cause is a deliberate concurrency/quorum
optimization in the Studio consensus implementation. There is no contract defect here
and no contract correction required. The separately verified phase-4 disagreement/rollback
behavior remains out of scope. Production main is unchanged; no work on phase 6.
