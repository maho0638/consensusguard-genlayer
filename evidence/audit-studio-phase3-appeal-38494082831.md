# ConsensusGuard local Studio phase-3 five-validator appeal lifecycle

GitHub Actions run: 38494082831
Test scope: deploy, open_case, resolve, and appeal with independent consensus; rollback out of scope.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x35c65479f581a2b61cae7c0b1bf556a75b45f647ccd300f7b12cff749140dda9 status=UNKNOWN finalized
- WAIT_DONE: 0x35c65479f581a2b61cae7c0b1bf556a75b45f647ccd300f7b12cff749140dda9 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x9fb18da410646cddeb1366aa45646b9a8eff7fccff128f2314c6baabe7eb2e10 status=UNKNOWN finalized
- WAIT_DONE: 0x9fb18da410646cddeb1366aa45646b9a8eff7fccff128f2314c6baabe7eb2e10 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0x914616db7aba2d425d9349fcdfa9f92d74ece4bc98b125ae20742cac01c1a158 status=UNKNOWN finalized
- WAIT_DONE: 0x914616db7aba2d425d9349fcdfa9f92d74ece4bc98b125ae20742cac01c1a158 status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=SUCCESS vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: 
- STUDIO_RESOLVE_VM_ERROR_COUNT: 0
- STUDIO_RESOLVE_SAFE_CASE_STATE: DECIDED
- STUDIO_SAFE_VOTE_COUNTS: agree=3 idle=2 unexpected=0

## Local transaction state summaries
- TX_STATE|FINALIZED|count=3
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=1
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=2
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object
- LIFECYCLE|total=3|finalized=3|unfinalized=0|write_calls=2

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
