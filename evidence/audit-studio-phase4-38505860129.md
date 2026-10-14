# Phase 4 — independent local Studio 5-validator disagreement and rollback

CI run: 38505860129
CI head SHA: e8022da8c14edf30dde0a56894e9ba1fd964c863
Scope: first verify exhausted 5-validator pool (2/2/1); then verify a 5-member committee with one spare 6th validator (2/2/2) can rotate.
Required: real dissent, unchanged OPEN state and successful retry in both tests; rotation_count=0 with no spare, rotation_count>=1 with six-validator pool. FINALIZED is a lifecycle status.
This is local Studio, NOT Bradbury; validator secrets and raw transaction receipts are excluded.

## Safe checkpoints
- PHASE4_READY: five validators, 2/2/1 conflicting responses
- PHASE4_DISAGREEMENT_START
- PHASE4_WAIT_RETURNED
- PHASE4_DISAGREEMENT_TX: 0xc27d56a45566220093d662501b0cb1abaa70e9835756ed662efb2805c7356da3
- PHASE4_RECEIPT_STATUS: UNKNOWN
- PHASE4_CONSENSUS_KEYS: leader_receipt,validators,votes
- PHASE4_VOTES: agree=1 disagree=3 idle=1 other=0
- PHASE4_CHAIN_STATE: state=OPEN decisions=0
- PHASE4_RPC_STATUS: FINALIZED
- PHASE4_HISTORY_ROUNDS: Undetermined
- PHASE4_ROTATION_COUNT: 0
- PHASE4_NO_SPARE_ROTATION: count=0 terminal=Undetermined
- PHASE4_ROLLBACK_STATE: OPEN decisions=0 case_unchanged=true
- PHASE4_RECOVERY_START
- PHASE4_RECOVERY_TX: 0xb4afa883f46e2f6a27d19dd2116d9575a63bddd73099f06b40f315539655fe1c
- PHASE4_RECOVERY_STATE: DECIDED decisions=1 outcome=VERIFIED
- PHASE4_COMPLETE: REAL_STUDIO_DISAGREEMENT_ROLLBACK_RECOVERY_PASS
- PHASE4_ROTATION_READY: five-member committee drawn from six validators with 2/2/2 conflicting responses
- PHASE4_DISAGREEMENT_START
- PHASE4_WAIT_RETURNED
- PHASE4_DISAGREEMENT_TX: 0xd32b15a319b84f8795cfdd49e1bd43d130175f17d92817152adfbc651c8e474e
- PHASE4_RECEIPT_STATUS: UNKNOWN
- PHASE4_CONSENSUS_KEYS: leader_receipt,validators,votes
- PHASE4_VOTES: agree=2 disagree=3 idle=0 other=0
- PHASE4_CHAIN_STATE: state=OPEN decisions=0
- PHASE4_RPC_STATUS: FINALIZED
- PHASE4_HISTORY_ROUNDS: Leader Rotation,Undetermined
- PHASE4_ROTATION_COUNT: 1
- PHASE4_ROLLBACK_STATE: OPEN decisions=0 case_unchanged=true
- PHASE4_RECOVERY_START
- PHASE4_RECOVERY_TX: 0xef9257a630d36c9d9e9a52aadd6989d7a83eade94e03b3e6b3823e2ffc1d9f36
- PHASE4_RECOVERY_STATE: DECIDED decisions=1 outcome=VERIFIED
- PHASE4_ROTATION_COMPLETE: REAL_STUDIO_SPARE_VALIDATOR_ROTATION_ROLLBACK_RECOVERY_PASS

## Database state summary
- TX_STATE|FINALIZED|count=8
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=2
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=6
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object
- LIFECYCLE|total=8|finalized=8|unfinalized=0|write_calls=6

## Worker stage counts
- WORKER_STAGE|finalization_started|count=8
- WORKER_STAGE|finalization_done|count=8
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
PASS
