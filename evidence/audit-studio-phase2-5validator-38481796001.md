# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38481796001
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x4bf596690d7460f3db6f6c754ad369e4700f1003f1192ce2edf153dd28671f1d status=UNKNOWN finalized
- WAIT_DONE: 0x4bf596690d7460f3db6f6c754ad369e4700f1003f1192ce2edf153dd28671f1d status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x2d6a9ee39399dd27b880a0196e8a5dc62d30b31834f1bb1e613a2cb1edce6fdd status=UNKNOWN finalized
- WAIT_DONE: 0x2d6a9ee39399dd27b880a0196e8a5dc62d30b31834f1bb1e613a2cb1edce6fdd status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0x2faa5e6d1100f72f8e3acd73a0fa6c41a9138e295ada4d61f9b01c45ae86d1be status=UNKNOWN finalized
- WAIT_DONE: 0x2faa5e6d1100f72f8e3acd73a0fa6c41a9138e295ada4d61f9b01c45ae86d1be status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=ERROR vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: 
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
