# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38491259396
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xcd1bd9c94d14bb458da6227f8b628e8171eb0678833b7b39becf0cebbcafa687 status=UNKNOWN finalized
- WAIT_DONE: 0xcd1bd9c94d14bb458da6227f8b628e8171eb0678833b7b39becf0cebbcafa687 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x12bf2464927281dc2b439a9df8e793fc8085203cf785cd63b8be7071003536a5 status=UNKNOWN finalized
- WAIT_DONE: 0x12bf2464927281dc2b439a9df8e793fc8085203cf785cd63b8be7071003536a5 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0x2fb5f26e82954972e8d8d4099411d49dbb8b50f2d2efed169d039b836ed9f515 status=UNKNOWN finalized
- WAIT_DONE: 0x2fb5f26e82954972e8d8d4099411d49dbb8b50f2d2efed169d039b836ed9f515 status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED
- PHASE: FIVE_VALIDATOR_RESOLVE_PASS

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=SUCCESS vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: 
- STUDIO_RESOLVE_VM_ERROR_COUNT: 0
- STUDIO_RESOLVE_SAFE_CASE_STATE: DECIDED

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
PASS
