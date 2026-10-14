# ConsensusGuard phase five: true idle-cancellation root cause (local Studio)

GitHub Actions run: 38532431448
Test scope: five validator Studio resolve and appeal, exactly three agree, two synthetic idle each. No Studio Dev replay.
No validator identities, configs, secrets or raw receipts included; local Studio only.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x905769672b3a35ebb11e2eff766d418206f0cb173bbb6c4e22c37214e25c8768 status=UNKNOWN finalized
- WAIT_DONE: 0x905769672b3a35ebb11e2eff766d418206f0cb173bbb6c4e22c37214e25c8768 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0xbf3aad1c532255ea128a57367e25930fd641599d0e5bf841e30d6b64018fcfe9 status=UNKNOWN finalized
- WAIT_DONE: 0xbf3aad1c532255ea128a57367e25930fd641599d0e5bf841e30d6b64018fcfe9 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0x2e71f9b9e810f46b3e32b152e078b366d27320d69967e6daf17dd6fcec17a985 status=UNKNOWN finalized
- WAIT_DONE: 0x2e71f9b9e810f46b3e32b152e078b366d27320d69967e6daf17dd6fcec17a985 status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED
- PHASE: FIVE_VALIDATOR_QUORUM_VERIFIED
- PHASE: FIVE_VALIDATOR_RESOLVE_PASS
- PHASE: APPEAL_VALIDATORS_READY
- PHASE: APPEAL_START
- WAIT_START: 0xaedbca41bea2ba55386083ea1664736f4e9b30b147d804f65ade8cf3197cc374 status=UNKNOWN finalized
- WAIT_DONE: 0xaedbca41bea2ba55386083ea1664736f4e9b30b147d804f65ade8cf3197cc374 status=UNKNOWN 
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
- STUDIO_PHASE5_IDLE_PROOF: RESOLVE agree=3 idle=2 synthetic_quorum_cancellations=2 fatal=0 unexplained_idle=0
- STUDIO_SAFE_APPEAL_VOTE_COUNTS: agree=3 idle=2 unexpected=0
- STUDIO_PHASE5_IDLE_PROOF: APPEAL agree=3 idle=2 synthetic_quorum_cancellations=2 fatal=0 unexplained_idle=0
- STUDIO_PHASE5_COMPLETE: RESOLVE_AND_APPEAL_TWO_IDLE_CAUSE_PROVEN
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
