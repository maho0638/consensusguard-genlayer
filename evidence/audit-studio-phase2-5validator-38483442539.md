# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38483442539
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xe9bb0d76e901db16ca41259eb3ea69c5001cf39a1ce08cd20fa957a1aa2603a4 status=UNKNOWN finalized
- WAIT_DONE: 0xe9bb0d76e901db16ca41259eb3ea69c5001cf39a1ce08cd20fa957a1aa2603a4 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x82cc54515de93e210a92033e36f2b92ac69734257cd91b9239a2b3e78b3dab6e status=UNKNOWN finalized
- WAIT_DONE: 0x82cc54515de93e210a92033e36f2b92ac69734257cd91b9239a2b3e78b3dab6e status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0xba6f3bbfeda600689701a8f4949fbb31a623808d88816c58670644d2a94b21bc status=UNKNOWN finalized
- WAIT_DONE: 0xba6f3bbfeda600689701a8f4949fbb31a623808d88816c58670644d2a94b21bc status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=ERROR vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: invalid,json,response,contract,exception
- STUDIO_RESOLVE_SAFE_CASE_STATE: OPEN

## Local transaction state summaries
- TX_STATE|FINALIZED|count=3
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=1
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=2
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object

## Worker stages (counts only)
- WORKER_STAGE|finalization_started|count=3
- WORKER_STAGE|finalization_done|count=3
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
NOT YET CONFIRMED / FAILED
