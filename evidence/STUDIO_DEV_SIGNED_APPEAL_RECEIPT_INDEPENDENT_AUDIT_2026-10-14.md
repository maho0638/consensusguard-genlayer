# Fresh verified Studio Dev appeal: independent original transaction audit

CI https://github.com/maho0638/consensusguard-genlayer/actions/runs/38583016128
Original successful signed test run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38575792658
Read-only evidence; no private account data, re-deploy, funding, GEN spend or transaction submission.

## Deployed code identity
- Correct chain 61997: True
- Deployed source SHA-256: \`bcf15ef524a1b108480e3ab8a178d0b2ff561440b9de930ea949344cdc1f0a0f\`
- Current audited source SHA-256: \`bcf15ef524a1b108480e3ab8a178d0b2ff561440b9de930ea949344cdc1f0a0f\`
- Deployed source EXACT match: **True**
- Explorer contract transaction count: 4

## Signed transaction receipts
- deploy: status=FINALIZED, execution=FINISHED_WITH_RETURN, result=None, votes={"agree": 3, "idle": 2}
  - full consensus votes: {"agree": 3, "idle": 2}
  - consensus fields present=3
- open_case: status=FINALIZED, execution=FINISHED_WITH_RETURN, result=None, votes={"agree": 3, "idle": 2}
  - full consensus votes: {"agree": 3, "idle": 2}
  - consensus fields present=3
- resolve: status=FINALIZED, execution=FINISHED_WITH_RETURN, result=None, votes={"agree": 3, "disagree": 1, "idle": 1}
  - full consensus votes: {"agree": 3, "disagree": 1, "idle": 1}
  - consensus fields present=3
- appeal: status=FINALIZED, execution=FINISHED_WITH_RETURN, result=None, votes={"agree": 3, "disagree": 1, "idle": 1}
  - full consensus votes: {"agree": 3, "disagree": 1, "idle": 1}
  - consensus fields present=3

- FINISHED_WITH_RETURN and FINALIZED count: 4/4
- All four strong receipt gates pass: **True**

## State proof boundary
A full signed, successful FINALIZED contract-level appeal plus source identity
establishes the contract's appeal() method was actually executed successfully,
but the independent get_case/get_decision readback is currently inaccessible:
the Studio Dev gen_call backend returns SQLAlchemy invalid session rollback -32603.
Thus actual historic state mutation follows successful application execution and
the exact tested contract, but JSON readback is NOT claimed to have succeeded.
