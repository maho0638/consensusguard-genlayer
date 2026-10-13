# ConsensusGuard local Studio phase-1 diagnostic

GitHub Actions run: 38468870190
Test scope: deployment and open_case ONLY; no resolve or appeal.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x8a459b4109e6d7ff3f738387af086fb58b0e0b15646e09c2a03083fa7b5cf2d7 status=UNKNOWN finalized
- WAIT_FAILURE: 0x8a459b4109e6d7ff3f738387af086fb58b0e0b15646e09c2a03083fa7b5cf2d7 status=UNKNOWN GenLayerError

## Local transaction state summaries
- TX_STATE|ACCEPTED|count=1
- TX_DETAIL|ACCEPTED|type=1|mode=NORMAL|timestamp_missing=false|blocked=true|address_missing=false|count=1
- TX_AGE|status=ACCEPTED|since_accepted=150|blocked_for=151|appeal_deadline_delta=-120

## Worker stages (counts only)
- WORKER_STAGE|finalization_started|count=0
- WORKER_STAGE|finalization_done|count=0
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
NOT YET CONFIRMED / FAILED
