# ConsensusGuard — Studio Dev real appeal: verified external blocker
Date: 2026-10-14

## Direct conclusion

**The ConsensusGuard contract is not known to be defective.**
Its contract-level `appeal(0, new_manifest_json)` passed a true local Studio
5-validator transaction test and append-only state readback (phase 3, phase 6).
But **the original deployed contract's signed Studio Dev appeal has not been
submitted or proven**. Therefore the claim "every possible real-network check
was done" would be false.

### Exact remote evidence (official chain ID 61997)

- Historical Studio Dev `resolve` transaction
  `0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9`
  is retrievable and `FINALIZED`.
- Contract: `0xBa84783D71d902c8BD3Ba63418Df172280249139`.
- Hosted RPC chain identity is `61997`, not Studionet `61999`.
- Matched SDK 0.19.0rc2 `read_contract(get_case, 0)` failed with
  `gen_call -32603`: **"Can't reconnect until invalid transaction is rolled
  back. Please rollback() fully before proceeding"** (SQLAlchemy 8s2b).
  That error was reproduced for the non-final snapshot and also when
  explicitly selecting `TransactionHashVariant.LATEST_FINAL`.
- Fallback JSON-RPC `gen_getContractState` returned `-32601 Method not found`
  for both accepted and finalized state. This remote endpoint does not expose
  that method; a successful local-node API call must not be assumed.
- Historical Explorer transaction endpoint is reachable.
- The schema-by-address probe was not a valid replacement for `get_case`
  because `gen_getContractSchema` expects source code, not a contract-address
  dict; the resulting psycopg2 can't-adapt-dict was a request-shape error,
  not evidence of any contract bug.
- No remote request in this diagnosis signed or broadcast any transaction,
  deployed/replaced a contract, connected a user's wallet, or spent GEN.

## What actually blocks the last live check

1. **External server problem:** Studio Dev's `gen_call` cannot currently return
   the read state for this contract because the **Studio Dev service's database
   transaction session** reports a pending rollback. Only the Studio Dev
   operator can repair/reset the failing server-side database connection
   handling. This GitHub workspace and contract repository cannot administer
   that hosted service.
2. **Request authorization:** the smart-contract `appeal()` method verifies
   `gl.message.sender_address == case.requester`. The original requester
   is an external test-wallet account held by the user (and correctly not
   checked into source control or exposed to the assistant). Without the
   user's original wallet signature, GitHub CI may not validly act as
   that address. A random new account will revert with
   "only requester may appeal"; a local mock proof cannot substitute for
   an authenticated public Studio Dev write.

This must not be confused with **protocol-level** `appealTransaction(txId)`.
The missing test is the contract's own one-time `appeal(case_id=0, new_manifest_json)`
and finalized `get_case(0)`, `get_decision(0/1)` read-back.

## Final gate and recovery

Once the Studio Dev host API is healthy, use the **same test wallet** that
created case 0 in Studio Dev, import the existing contract by address, and
submit its **contract-level** `appeal` method (case_id `0`, valid two-host
manifest with correct SHA-256 commitments), confirm the wallet transaction,
then wait until `FINALIZED`. Check exact case state `APPEALED`,
`appeal_used=true`, `decision_count=2`, latest decision round 1,
first decision at index 0 unchanged, and distinct manifest commitments.
Capture the actual new transaction ID and sanitized receipts to close the
last evidence requirement.

**Verdict: Studio Dev live appeal BLOCKED and UNVERIFIED.
Local contract regression PASS. No permission or authority to claim completion.**

## Proof

- Official GitHub CI read-only diagnostic: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38569130229
- Official GitHub CI finalized snapshot retry: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38569352345
- See `evidence/STUDIO_DEV_APPEAL_LIVE_PREFLIGHT_2026-10-14.md`,
  `evidence/STUDIO_DEV_RPC_BACKEND_DIAGNOSTICS_2026-10-14.md`.
- Local 3-test real Studio run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38555170256
