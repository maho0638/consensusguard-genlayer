# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38485097915
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x6f1843048e89b66d84fa5af836182d3548cb94eaa4728d6f3ea8d1d431e4f1cf status=UNKNOWN finalized
- WAIT_DONE: 0x6f1843048e89b66d84fa5af836182d3548cb94eaa4728d6f3ea8d1d431e4f1cf status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0xd1a1b1d3fe309df64769b96148a053a0a5d1545b542a43ba85b6444e3658114e status=UNKNOWN finalized
- WAIT_DONE: 0xd1a1b1d3fe309df64769b96148a053a0a5d1545b542a43ba85b6444e3658114e status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0xfc9249f5d805541c2c3906dc3576995286176cc5b513f16b3284595344e74ffb status=UNKNOWN finalized
- WAIT_DONE: 0xfc9249f5d805541c2c3906dc3576995286176cc5b513f16b3284595344e74ffb status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=ERROR vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: invalid,json,response,contract,exception
- STUDIO_RESOLVE_VM_ERROR_COUNT: 0
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
