# ConsensusGuard local Studio phase-1 diagnostic

GitHub Actions run: 38470411424
Test scope: deployment and open_case ONLY; no resolve or appeal.
No validator configs, secrets or raw receipts are included.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x10c95466af1bd394dc92cb08d787704c785bb9aee35abe1dcec723c711fbaf96 status=UNKNOWN finalized
- WAIT_DONE: 0x10c95466af1bd394dc92cb08d787704c785bb9aee35abe1dcec723c711fbaf96 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x49bde0d2335850e94f7b555a13c0b0340c314f121eff55d10a32c462e9fee0fa status=UNKNOWN finalized
- WAIT_DONE: 0x49bde0d2335850e94f7b555a13c0b0340c314f121eff55d10a32c462e9fee0fa status=UNKNOWN 
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
