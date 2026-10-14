# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38490121928
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xdf132aa424a9ef1d414cdf763acd39643f631033f6b561044a87336e3441904d status=UNKNOWN finalized
- WAIT_DONE: 0xdf132aa424a9ef1d414cdf763acd39643f631033f6b561044a87336e3441904d status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0xda7eba3aca6e2d6fcd5f57af6f91cde62f95173811bac7c3f4a46f489403d3bb status=UNKNOWN finalized
- WAIT_DONE: 0xda7eba3aca6e2d6fcd5f57af6f91cde62f95173811bac7c3f4a46f489403d3bb status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0xd35b071839de545299a31343276f547e3dc954920cda03a1e5032dde9dff4758 status=UNKNOWN finalized
- WAIT_DONE: 0xd35b071839de545299a31343276f547e3dc954920cda03a1e5032dde9dff4758 status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED

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
NOT YET CONFIRMED / FAILED
