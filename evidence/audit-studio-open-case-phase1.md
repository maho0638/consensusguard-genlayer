# ConsensusGuard local Studio phase-1 diagnostic

GitHub Actions run: 38474606747
Test scope: deployment and open_case ONLY; no resolve or appeal.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xc2fad4d280b06fd6c46dde6898f6865b3efd037c85f31645c3880da94290b029 status=PENDING finalized
- WAIT_FAILURE: 0xc2fad4d280b06fd6c46dde6898f6865b3efd037c85f31645c3880da94290b029 status=ACCEPTED GenLayerError

## Local transaction state summaries
- TX_STATE|ACCEPTED|count=1
- TX_DETAIL|ACCEPTED|type=1|mode=NORMAL|timestamp_missing=false|blocked=true|address_missing=false|count=1
- TX_AGE|status=ACCEPTED|since_accepted=270|blocked_for=270|appeal_deadline_delta=-240

## Worker stages (counts only)
- WORKER_STAGE|finalization_started|count=0
- WORKER_STAGE|finalization_done|count=0
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3
- WORKER_STAGE|transaction_processed|count=0
- WORKER_STAGE|temporary_validator_configured|count=15
- WORKER_STAGE|contract_deployed|count=1

## Result
NOT YET CONFIRMED / FAILED
