# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38491286051
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xf96b379dbbb6ae24e5d1d0b8ede6ade26312667c7decc46b2423afb12ff500fb status=UNKNOWN finalized
- WAIT_DONE: 0xf96b379dbbb6ae24e5d1d0b8ede6ade26312667c7decc46b2423afb12ff500fb status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x2ed7878f8ec98bdacb975c2f46ed242f795c1f5cdd581110353a6b9c08c285d1 status=UNKNOWN finalized
- WAIT_DONE: 0x2ed7878f8ec98bdacb975c2f46ed242f795c1f5cdd581110353a6b9c08c285d1 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0x0ca0eec84f3c08e7ea04609989b7d09c5168a2e888f3964826a1b2bacb607f73 status=UNKNOWN finalized
- WAIT_DONE: 0x0ca0eec84f3c08e7ea04609989b7d09c5168a2e888f3964826a1b2bacb607f73 status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED
- PHASE: FIVE_VALIDATOR_QUORUM_VERIFIED
- PHASE: FIVE_VALIDATOR_RESOLVE_PASS

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
