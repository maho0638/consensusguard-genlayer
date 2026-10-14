# Phase 4 — independent local Studio 5-validator disagreement and rollback

CI run: 38503528542
CI head SHA: 5214b23d4167d6934f128bcacd507728bd5a7fba
Scope: controlled 2/2/1 mismatched LLM answers across five independent validator processes.
Required: three real disagree votes, recorded leader rotation, unchanged OPEN state, zero decisions, and successful retry. FINALIZED is a lifecycle status and does not prove state commitment.
This is local Studio, NOT Bradbury; validator secrets and raw transaction receipts are excluded.

## Safe checkpoints
- PHASE4_READY: five validators, 2/2/1 conflicting responses
- PHASE4_DISAGREEMENT_START
- PHASE4_WAIT_RETURNED
- PHASE4_DISAGREEMENT_TX: 0x9756b1b4265a2cbc85ed15becad7f6c75f98bfb3b008f864f2641a8e7f994377
- PHASE4_RECEIPT_STATUS: UNKNOWN
- PHASE4_CONSENSUS_KEYS: leader_receipt,validators,votes
- PHASE4_VOTES: agree=1 disagree=3 idle=1 other=0
- PHASE4_CHAIN_STATE: state=OPEN decisions=0
- PHASE4_RPC_STATUS: FINALIZED
- PHASE4_HISTORY_ROUNDS: Undetermined
- PHASE4_ROTATION_COUNT: 0

## Database state summary
- TX_STATE|FINALIZED|count=3
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=1
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=2
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object
- LIFECYCLE|total=3|finalized=3|unfinalized=0|write_calls=2

## Worker stage counts
- WORKER_STAGE|finalization_started|count=3
- WORKER_STAGE|finalization_done|count=3
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
NOT VERIFIED / FAILED
