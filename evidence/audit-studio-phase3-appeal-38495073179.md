# ConsensusGuard local Studio phase-3 five-validator appeal lifecycle

GitHub Actions run: 38495073179
Test scope: deploy, open_case, resolve, and appeal with independent consensus; rollback out of scope.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x57e2a3c77bfa498d64a7030c832747f21e4ec70af343014530b173dea9d4585b status=UNKNOWN finalized
- WAIT_DONE: 0x57e2a3c77bfa498d64a7030c832747f21e4ec70af343014530b173dea9d4585b status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x8104e6ae357e11d63853a414c8b1ab1af0ffff139ca290ae855974b89ad60c5b status=UNKNOWN finalized
- WAIT_DONE: 0x8104e6ae357e11d63853a414c8b1ab1af0ffff139ca290ae855974b89ad60c5b status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0xc916d8392dc365995de578cbf7bb7428fe741081cd9764158596c912468304b3 status=UNKNOWN finalized
- WAIT_DONE: 0xc916d8392dc365995de578cbf7bb7428fe741081cd9764158596c912468304b3 status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED
- PHASE: FIVE_VALIDATOR_QUORUM_VERIFIED
- PHASE: FIVE_VALIDATOR_RESOLVE_PASS
- PHASE: APPEAL_VALIDATORS_READY
- PHASE: APPEAL_START
- WAIT_START: 0xa636107cb96249b458cc843ca9a540a6d5032d71a317f363e370136bc6514f8d status=UNKNOWN finalized
- WAIT_DONE: 0xa636107cb96249b458cc843ca9a540a6d5032d71a317f363e370136bc6514f8d status=UNKNOWN 
- PHASE: APPEAL_FINALIZED
- PHASE: APPEAL_QUORUM_VERIFIED
- PHASE: APPEAL_HISTORY_VERIFIED
- PHASE: FULL_APPEAL_LIFECYCLE_PASS

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=SUCCESS vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: 
- STUDIO_RESOLVE_VM_ERROR_COUNT: 0
- STUDIO_RESOLVE_SAFE_CASE_STATE: DECIDED
- STUDIO_SAFE_VOTE_COUNTS: agree=3 idle=2 unexpected=0
- STUDIO_SAFE_APPEAL_VOTE_COUNTS: agree=3 idle=2 unexpected=0
- STUDIO_SAFE_APPEAL_RESULT: state=APPEALED old=VERIFIED new=REJECTED decisions=2

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
PASS
