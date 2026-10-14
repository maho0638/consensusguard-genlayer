# ConsensusGuard local Studio phase-3 five-validator appeal lifecycle

GitHub Actions run: 38493041726
Test scope: deploy, open_case, resolve, and appeal with independent consensus; rollback out of scope.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xe90b4d9df8578c05c5356bb0d6899b5b6037fa4b956de93c26a039a46dc7699c status=UNKNOWN finalized
- WAIT_DONE: 0xe90b4d9df8578c05c5356bb0d6899b5b6037fa4b956de93c26a039a46dc7699c status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x866400662ef53ec3158a941721f42158a9dad7ec8a70ae1b005afc3ed7e76e3d status=UNKNOWN finalized
- WAIT_DONE: 0x866400662ef53ec3158a941721f42158a9dad7ec8a70ae1b005afc3ed7e76e3d status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0x388f6aa3ddc8e9ad7ae79bb7d5842b516cbb3bb6e70f6261ab4a1b4c6a054fa5 status=UNKNOWN finalized
- WAIT_DONE: 0x388f6aa3ddc8e9ad7ae79bb7d5842b516cbb3bb6e70f6261ab4a1b4c6a054fa5 status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED
- PHASE: FIVE_VALIDATOR_QUORUM_VERIFIED
- PHASE: FIVE_VALIDATOR_RESOLVE_PASS
- PHASE: APPEAL_VALIDATORS_READY
- PHASE: APPEAL_START
- WAIT_START: 0x9999d97aa4bc927bd7cf0920bbe41032d8e603c09df9c9178fb0657455fbc98e status=UNKNOWN finalized
- WAIT_DONE: 0x9999d97aa4bc927bd7cf0920bbe41032d8e603c09df9c9178fb0657455fbc98e status=UNKNOWN 
- PHASE: APPEAL_FINALIZED

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=SUCCESS vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: 
- STUDIO_RESOLVE_VM_ERROR_COUNT: 0
- STUDIO_RESOLVE_SAFE_CASE_STATE: DECIDED
- STUDIO_SAFE_VOTE_COUNTS: agree=3 idle=2 unexpected=0
- STUDIO_SAFE_APPEAL_VOTE_COUNTS: agree=3 idle=2 unexpected=0

## Local transaction state summaries
- TX_STATE|FINALIZED|count=4
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=1
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=3
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object
- LIFECYCLE|total=4|finalized=4|unfinalized=0|write_calls=3

## Worker stages (counts only)
- WORKER_STAGE|finalization_started|count=4
- WORKER_STAGE|finalization_done|count=4
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
NOT YET CONFIRMED / FAILED
