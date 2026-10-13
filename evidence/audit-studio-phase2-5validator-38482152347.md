# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38482152347
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x9d42374bd15b5f446404861e6471e21a6320b64892f962002cd32809a29dedcc status=UNKNOWN finalized
- WAIT_DONE: 0x9d42374bd15b5f446404861e6471e21a6320b64892f962002cd32809a29dedcc status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0xe9fb864506a907dc1543fe36e4b582b719be4a8050f3056541f0a238ad954818 status=UNKNOWN finalized
- WAIT_DONE: 0xe9fb864506a907dc1543fe36e4b582b719be4a8050f3056541f0a238ad954818 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0xb1b084b7b3eaf8ca70f48e306d605251ca043b2b16e250cdbcfa765cd1f23f15 status=UNKNOWN finalized
- WAIT_DONE: 0xb1b084b7b3eaf8ca70f48e306d605251ca043b2b16e250cdbcfa765cd1f23f15 status=UNKNOWN 
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
