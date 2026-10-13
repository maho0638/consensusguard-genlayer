# ConsensusGuard local Studio phase-2 five-validator integration

GitHub Actions run: 38483628129
Test scope: deploy, open_case and nondeterministic resolve; no appeal or rollback.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x47eeb7e983cdeb344b02266c82941b2d58d5ec32a58bdc14f7913f0b12ec9acc status=UNKNOWN finalized
- WAIT_DONE: 0x47eeb7e983cdeb344b02266c82941b2d58d5ec32a58bdc14f7913f0b12ec9acc status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x64cb56d7f884487e5c88d0692ff8bde9b68ac97cea6249173037a3c40f7ccc70 status=UNKNOWN finalized
- WAIT_DONE: 0x64cb56d7f884487e5c88d0692ff8bde9b68ac97cea6249173037a3c40f7ccc70 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0x9bd975a2890683d295820808bfd1fb6f9df085ba830270c047b305aefab5181b status=UNKNOWN finalized
- WAIT_DONE: 0x9bd975a2890683d295820808bfd1fb6f9df085ba830270c047b305aefab5181b status=UNKNOWN 
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
