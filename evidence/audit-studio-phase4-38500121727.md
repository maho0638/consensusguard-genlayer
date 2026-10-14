# Phase 4 — independent local Studio 5-validator disagreement and rollback

CI run: 38500121727
CI head SHA: 336e62536d3d0d8c079951f81f614dd6e0db9500
Scope: controlled 2/2/1 mismatched LLM answers across five independent validator processes.
Required: UNDETERMINED, at least one real disagree vote, OPEN state, decision_count=0, and successful retry.
This is local Studio, NOT Bradbury; validator secrets and raw transaction receipts are excluded.

## Safe checkpoints
- PHASE4_READY: five validators, 2/2/1 conflicting responses
- PHASE4_DISAGREEMENT_START
- PHASE4_WAIT_RETURNED
- PHASE4_DISAGREEMENT_TX: 0x0c2588248ed21cf2d0508b6154ced24bd884666c553b6152c99235f4a0c053f4
- PHASE4_RECEIPT_STATUS: UNKNOWN
- PHASE4_CONSENSUS_KEYS: leader_receipt,validators,votes
- PHASE4_VOTES: agree=2 disagree=3 idle=0 other=0
- PHASE4_CHAIN_STATE: state=OPEN decisions=0
- PHASE4_RPC_STATUS: FINALIZED
- PHASE4_HISTORY_ROUNDS: 
- PHASE4_ROTATION_COUNT: UNAVAILABLE
- PHASE4_ROLLBACK_STATE: OPEN decisions=0 case_unchanged=true
- PHASE4_RECOVERY_START
- PHASE4_RECOVERY_TX: 0x24bd3c0ab3224c3e6f94a48d4c605d4af88f95e50b2e206a5cef4ef7dcdb3ef4
- PHASE4_RECOVERY_STATE: DECIDED decisions=1 outcome=VERIFIED
- PHASE4_COMPLETE: REAL_STUDIO_DISAGREEMENT_ROLLBACK_RECOVERY_PASS

## Database state summary
- TX_STATE|FINALIZED|count=4
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=1
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=3
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object
- LIFECYCLE|total=4|finalized=4|unfinalized=0|write_calls=3

## Worker stage counts
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
