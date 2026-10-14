# ConsensusGuard — FINAL Studio Dev signed appeal verification (2026-10-14)

## Latest verified outcome

**SIGNED CONTRACT APPEAL: PASS ON REAL STUDIO DEV CHAIN 61997.**

The one-time GitHub Actions end-to-end job `38575792658` submitted four
independently signed transactions using an ephemeral test account to
GenLayer **Studio Dev** (not Bradbury main testnet). They were:

| operation | hash | execution |
|---|---|---|
| deploy | `0x02a61d2045383a5006481444b227b54a6b2002928eb57bd8a34181b990533acb` | FINALIZED, FINISHED_WITH_RETURN |
| open_case | `0x32b17766f999e7f103421636a247f96737ecec6647d4041f54538c3e460ca4ad` | FINALIZED, FINISHED_WITH_RETURN |
| resolve | `0xf837ea892a8a7ddc722dd4b2db7ab9096b654cf201aa47b6bc85600799534495` | FINALIZED, FINISHED_WITH_RETURN |
| **appeal** | `0xfd9bcbfcd01112deb5eb074c8e0bc9be1ff0d7e1a875d4fa953fb2e2f2a889e8` | **FINALIZED, FINISHED_WITH_RETURN** |

**Deployed contract address:**
`0x06C85d37A4937659585D6855839659B45ebC3E46`.

**Provenance**: Current audit contract file has exact deployed source
SHA-256 `bcf15ef524a1b108480e3ab8a178d0b2ff561440b9de930ea949344cdc1f0a0f`.
Independent Explorer retrieval matches the GitHub byte-for-byte source.
No old 2026-10-12 contract substitution.

**Validator outcomes** verified in a second, independent read-only CI
with both standard RPC and GenLayer full transaction receipt:
- deploy: 3 agree, 2 idle
- open_case: 3 agree, 2 idle
- resolve: 3 agree, 1 disagree, 1 idle
- **appeal: 3 agree, 1 disagree, 1 idle**.

All four reached successful execution, not merely chain-level FINALIZED status.
This is a 3-of-5 accepted consensus; it does **not** claim unanimous
validator agreement. The 1 disagree vote is not silently concealed.

The approved test used a GitHub CI-generated ephemeral account funded
through the Studio Dev simulator with **1 test GEN maximum**. The user
wallet/private key was **never accessed**, and no mainnet, Vercel,
Portal submission, main merge, or contract upgrade was performed.

## Exact boundary — remaining hosted Studio problem

The post-appeal contract `get_case(0)`, `get_decision(0/1)`,
`get_latest_decision(0)`, and `decision_count()` readback failed because
Studio Dev's RPC GenVM read route `gen_call` returned
`-32603: Can't reconnect until invalid transaction is rolled back`
(SQLAlchemy invalid DB transaction).

This failure occurred **after all four successful signed transactions**.
It is **not** evidence the `appeal` write reverted. The original
GitHub run is marked **failure** strictly because the test's mandatory
readback assertion raised that external RPC error.

The audited contract's `appeal` implementation checks requester-only,
DECIDED state and no prior appeal, then calls `_reach_decision(..., round=1)`
and, on successful non-reverted execution, appends a new decision and
sets `case.state = "APPEALED"` and `case.appeal_used = True`.
Consequently the successful `FINISHED_WITH_RETURN` appeal receipt
supports the expected state transition **by verified contract semantics**,
but independent storage readback has not been acquired. **Do not mislabel
contract-state JSON readback as PASS.**

Our exploratory read-only checks via `gen_call`, `sim_call`, `eth_call`,
and the separate Explorer RPC proxy all reproduced the same hosted server
error. The external server's SQLAlchemy DB session cannot be repaired by
modifying ConsensusGuard's contract source. The new ephemeral signing key
was deliberately not persisted: no duplicate re-deployment should be
performed to re-prove the already successful appeal.

## Links, evidence and final gate

- <https://github.com/maho0638/consensusguard-genlayer/actions/runs/38575792658>
  — original one-time signed real Studio Dev test (four writes PASS, later readback FAIL).
- <https://github.com/maho0638/consensusguard-genlayer/actions/runs/38583016128>
  — independent **SUCCESS** receipt/source validator, no new writes.
- `evidence/STUDIO_DEV_PHASE7_SIGNED_APPEAL_2026-10-14.md`
- `evidence/STUDIO_DEV_SIGNED_APPEAL_RECEIPT_INDEPENDENT_AUDIT_2026-10-14.md`
- Last audited Quality CI: `38583015848` — SUCCESS, 98 offline PASS / 3 local Studio opt-in SKIP,
  and dedicated three-test local Studio integration PASS in run `38555170256`.

**Decision: Real signed Studio Dev contract-level appeal PASSED.
Current-source deploy, open_case, resolve, appeal PASSED.
Hosted Studio Dev get_case/get_decision readback remains BLOCKED, not PASSED.**

No claim that the network operator's database bug has been fixed. No further
deploys, faucet use, or GEN spent for the independent audit.
