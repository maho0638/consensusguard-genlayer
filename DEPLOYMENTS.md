# Deployment evidence

A deployment and Full Consensus transaction sequence was performed on 2026-10-12 in Studio Dev using a test wallet, after explicit user authorization. Exact transaction hashes, contract read-back, validator fields, and fee evidence are recorded in `evidence/studio-dev-live-validation.md`.

| Network | Status | Evidence |
|---|---|---|
| Localnet | Not run | No local GenLayer node was available in the coding workspace. |
| Studio Dev | Run | Deployment and `open_case`/`resolve` records reached consensus/finalization. Explorer reports five initial validators; the vote map is 3 `agree`, 2 `idle`; the resolve is `FINALIZED` and contract read-back is `VERIFIED`. |
| Public testnet (Studionet / Asimov / Bradbury) | Not run | No public testnet deployment is evidenced. Studio Dev is not represented as a public testnet. |
| Mainnet | Not run | No mainnet action or funds used. |

The Studio Dev resolve transaction's Explorer record reports an approximate fee of 0.000097 GEN. One earlier `open_case` attempt finalized as a transaction but the contract call failed with `USER_ERROR: duplicate source host`; that failure is documented as such. No Portal submission has been made. Real Studio consensus evidence does not prove factual truth, source independence, or five successful validator executions: see the detailed execution/vote caveats in the evidence record.
