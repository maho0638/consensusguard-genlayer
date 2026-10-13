# ConsensusGuard local Studio phase-1 diagnostic

GitHub Actions run: 38474767527
Test scope: deployment and open_case ONLY; no resolve or appeal.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x5b8a1d8ee3fa9d7299f01a8c12748188d4b9dc0fbc63182f698fe45a23b1fe06 status=UNKNOWN finalized
- WAIT_DONE: 0x5b8a1d8ee3fa9d7299f01a8c12748188d4b9dc0fbc63182f698fe45a23b1fe06 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x9a1b3dbfa3aaff152c1ed8f9f99b8881ae384ac1e65e4c00f468df1a77f10a1b status=UNKNOWN finalized
- WAIT_DONE: 0x9a1b3dbfa3aaff152c1ed8f9f99b8881ae384ac1e65e4c00f468df1a77f10a1b status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: PHASE1_OPEN_CASE_PASS

## Local transaction state summaries
- TX_STATE|FINALIZED|count=2
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=1
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=1

## Worker stages (counts only)
- WORKER_STAGE|finalization_started|count=2
- WORKER_STAGE|finalization_done|count=2
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
PASS
