# ConsensusGuard phase 3: real Studio OPEN → DECIDED → APPEALED

**Verdict: PASS for phase-3 scope (five-validator Studio localnet)**

- GitHub Actions integration run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38495073179 — SUCCESS.
- Same-revision Quality run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38495073171 — SUCCESS, 68 passed, 1 skipped.
- Sanitized machine-generated transaction and consensus trace: [audit-studio-phase3-appeal-38495073179.md](audit-studio-phase3-appeal-38495073179.md).
- Tested branch: `audit/studio-phase3-appeal-20261014`; integration run head commit `f75a5fab` (prefix).
- Code blobs verified after the run: contract `ca4df13afea4accc90e858aab5f71cb420242c57`; Studio integration test `37e12ac595dcd3e9e91142b9878e1643704d0c2b`; CI workflow `58b9e9568c71039ea9383a4b2df3a64a7e6b5138`.

## Observed chain operations
All four distinct transactions finalized in one disposable, isolated Studio v0.123.0-rc.7 execution:

| Stage | Transaction hash | Outcome |
|---|---|---|
| Contract deployment | `0x57e2a3c77bfa498d64a7030c832747f21e4ec70af343014530b173dea9d4585b` | FINALIZED |
| `open_case` | `0x8104e6ae357e11d63853a414c8b1ab1af0ffff139ca290ae855974b89ad60c5b` | FINALIZED; OPEN |
| `resolve` | `0xc916d8392dc365995de578cbf7bb7428fe741081cd9764158596c912468304b3` | FINALIZED; DECIDED, VERIFIED |
| `appeal` | `0xa636107cb96249b458cc843ca9a540a6d5032d71a317f363e370136bc6514f8d` | FINALIZED; APPEALED, REJECTED |

All four were `FINALIZED` in the Studio SQL transaction-state table, with zero unfinalized and zero worker-blocked entries. Worker logs show four finalization starts and four completions, with no worker finalization errors.

## Validator consensus
- Exactly five distinct validator identities were configured in the isolated Studio consensus run.
- Both adjudications had **3 agree, 2 idle, 0 unexpected** votes, satisfying a genuine quorum (not a claim of 5/5 unanimity).
- Every `idle` was checked against the official Studio code `CONSENSUS_VALIDATOR_QUORUM_REACHED` in a matching synthetic receipt; early quorum cancellation is intentional and is not a negative vote.
- The appeal used a separate mock evidence set; each validator was instructed to fetch and classify the new evidence within its own execution.

## Contract state and evidence commitments
- Case transitioned `OPEN → DECIDED → APPEALED`. `appeal_used` became true, and the latest decision index became 1.
- First decision at index 0 remained **unchanged**: `VERIFIED`, round 0, two SHA-256 verified supporting sources.
- New decision at index 1 is `REJECTED`, round 1, two distinct SHA-256 verified refuting sources, reason `REFUTATION_THRESHOLD_MET`, two refutations, zero supports.
- Original case manifest and its SHA-256 commitment remained unchanged. Appeal has a distinct manifest SHA-256. Claim, criteria, requester, policy SHA-256, and previous decision history were checked for integrity.
- Exactly one case and two immutable decision records were verified.

## Boundaries
- This proves **real local GenLayer Studio five-validator consensus** with deterministic mock HTTP/LLM provider responses. It does not prove Bradbury public testnet execution, live third-party content, validator disagreement / rollback, or irreversible production deployment.
- Deliberate disagreement/rollback execution is **phase 4**, not performed for phase 3.
- No merge to `main`, public Portal resubmission, Vercel deployment, wallet signature or GEN token spend.
- The one-appeal guard is covered by direct-mode regression tests; this CI validates one successful appeal but does not send a second onchain rejected appeal transaction.

**Phase 3 is complete within the above explicitly tested scope.**
