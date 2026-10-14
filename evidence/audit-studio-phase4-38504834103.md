# Phase 4 — independent local Studio 5-validator disagreement and rollback

CI run: 38504834103
CI head SHA: 421f9b0891bb50c9028141a810aed1f40afdf3c2
Scope: first verify exhausted 5-validator pool (2/2/1); then verify a 5-member committee with one spare 6th validator (2/2/2) can rotate.
Required: real dissent, unchanged OPEN state and successful retry in both tests; rotation_count=0 with no spare, rotation_count>=1 with six-validator pool. FINALIZED is a lifecycle status.
This is local Studio, NOT Bradbury; validator secrets and raw transaction receipts are excluded.

## Safe checkpoints
- PHASE4_READY: five validators, 2/2/1 conflicting responses
- PHASE4_DISAGREEMENT_START
- PHASE4_WAIT_RETURNED
- PHASE4_DISAGREEMENT_TX: 0x0d5b22e64d88f58c66d578764a7ca1ce6d6ff2023fc571d92265e5966f71c5af
- PHASE4_RECEIPT_STATUS: UNKNOWN
- PHASE4_CONSENSUS_KEYS: leader_receipt,validators,votes
- PHASE4_VOTES: agree=2 disagree=3 idle=0 other=0
- PHASE4_CHAIN_STATE: state=OPEN decisions=0
- PHASE4_RPC_STATUS: FINALIZED
- PHASE4_HISTORY_ROUNDS: Undetermined
- PHASE4_ROTATION_COUNT: 0
- PHASE4_NO_SPARE_ROTATION: count=0 terminal=Undetermined
- PHASE4_ROLLBACK_STATE: OPEN decisions=0 case_unchanged=true
- PHASE4_RECOVERY_START
- PHASE4_RECOVERY_TX: 0xcd1f1fbb8d3f0f33482f89d2e7ba4e9d8349e04100413388cb8fca2b407bfba9
- PHASE4_RECOVERY_STATE: DECIDED decisions=1 outcome=VERIFIED
- PHASE4_COMPLETE: REAL_STUDIO_DISAGREEMENT_ROLLBACK_RECOVERY_PASS

## Database state summary
- TX_STATE|FINALIZED|count=6
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=2
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=4
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object
- LIFECYCLE|total=6|finalized=6|unfinalized=0|write_calls=4

## Worker stage counts
- WORKER_STAGE|finalization_started|count=6
- WORKER_STAGE|finalization_done|count=6
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
NOT VERIFIED / FAILED
