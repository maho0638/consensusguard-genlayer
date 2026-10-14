# ConsensusGuard phase six: complete real local Studio integration audit

GitHub Actions run: 38555170256
Test scope: five validator resolve and appeal; genuine dissent/rollback/recovery; six-validator leader rotation.
No validator identities, configs, secrets or raw receipts included; local Studio only, not public Dev.

## Safe phase and transaction status checkpoints
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0x56fe4f5a4568c9529608d3a7e2a80b7ca49d9b69258bd338e21f320299177cc8 status=UNKNOWN finalized
- WAIT_DONE: 0x56fe4f5a4568c9529608d3a7e2a80b7ca49d9b69258bd338e21f320299177cc8 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x53f9b40fa4a52cfee316882cb521d9d5e2fa0a9fbb370acc8231e26227433a69 status=UNKNOWN finalized
- WAIT_DONE: 0x53f9b40fa4a52cfee316882cb521d9d5e2fa0a9fbb370acc8231e26227433a69 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- PHASE: FIVE_DISTINCT_REGISTERED_VALIDATORS
- PHASE: FIVE_VALIDATOR_MOCKS_READY
- PHASE: RESOLVE_START
- WAIT_START: 0xfc317956c24f39487d5e6b3963b93859985ef4248471a0539d064c514409f25c status=UNKNOWN finalized
- WAIT_DONE: 0xfc317956c24f39487d5e6b3963b93859985ef4248471a0539d064c514409f25c status=UNKNOWN 
- PHASE: RESOLVE_FINALIZED
- PHASE: FIVE_VALIDATOR_QUORUM_VERIFIED
- PHASE: FIVE_VALIDATOR_RESOLVE_PASS
- PHASE: APPEAL_VALIDATORS_READY
- PHASE: APPEAL_START
- WAIT_START: 0x9ea45daf7503ea70b22ab8056752cac5bd907be6c89a65d7f500682eb538ca0b status=UNKNOWN finalized
- WAIT_DONE: 0x9ea45daf7503ea70b22ab8056752cac5bd907be6c89a65d7f500682eb538ca0b status=UNKNOWN 
- PHASE: APPEAL_FINALIZED
- PHASE: APPEAL_QUORUM_VERIFIED
- PHASE: APPEAL_HISTORY_VERIFIED
- PHASE: FULL_APPEAL_LIFECYCLE_PASS
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xc23b119dc317625b44aba5c08a7139da945c019f314c5701d12720d05c2f8e55 status=UNKNOWN finalized
- WAIT_START: 0xc23b119dc317625b44aba5c08a7139da945c019f314c5701d12720d05c2f8e55 status=UNKNOWN finalized
- WAIT_DONE: 0xc23b119dc317625b44aba5c08a7139da945c019f314c5701d12720d05c2f8e55 status=UNKNOWN 
- WAIT_DONE: 0xc23b119dc317625b44aba5c08a7139da945c019f314c5701d12720d05c2f8e55 status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0xfb37085242bef0aea993e724e05be23d1f150cd32db3800db78c5cfb854c3039 status=UNKNOWN finalized
- WAIT_START: 0xfb37085242bef0aea993e724e05be23d1f150cd32db3800db78c5cfb854c3039 status=UNKNOWN finalized
- WAIT_DONE: 0xfb37085242bef0aea993e724e05be23d1f150cd32db3800db78c5cfb854c3039 status=UNKNOWN 
- WAIT_DONE: 0xfb37085242bef0aea993e724e05be23d1f150cd32db3800db78c5cfb854c3039 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- WAIT_START: 0xbc8c5a9616ebb75a07f0866f528936b31c02c8e084b35d8b79d83b26bb571351 status=UNKNOWN finalized
- WAIT_START: 0xbc8c5a9616ebb75a07f0866f528936b31c02c8e084b35d8b79d83b26bb571351 status=UNKNOWN finalized
- WAIT_DONE: 0xbc8c5a9616ebb75a07f0866f528936b31c02c8e084b35d8b79d83b26bb571351 status=UNKNOWN 
- WAIT_DONE: 0xbc8c5a9616ebb75a07f0866f528936b31c02c8e084b35d8b79d83b26bb571351 status=UNKNOWN 
- WAIT_START: 0x337de1d680bc9794813e526605db5f17452221821c3d4aff44327450a2a237f5 status=UNKNOWN finalized
- WAIT_START: 0x337de1d680bc9794813e526605db5f17452221821c3d4aff44327450a2a237f5 status=UNKNOWN finalized
- WAIT_DONE: 0x337de1d680bc9794813e526605db5f17452221821c3d4aff44327450a2a237f5 status=UNKNOWN 
- WAIT_DONE: 0x337de1d680bc9794813e526605db5f17452221821c3d4aff44327450a2a237f5 status=UNKNOWN 
- PHASE: VALIDATORS_READY
- PHASE: FEES_QUOTED
- PHASE: DEPLOY_START
- WAIT_START: 0xb9454dacf5228fa9767d4e4d0106a2dd727365e6c4b7a74dc9625a62d0bac32f status=UNKNOWN finalized
- WAIT_START: 0xb9454dacf5228fa9767d4e4d0106a2dd727365e6c4b7a74dc9625a62d0bac32f status=UNKNOWN finalized
- WAIT_START: 0xb9454dacf5228fa9767d4e4d0106a2dd727365e6c4b7a74dc9625a62d0bac32f status=UNKNOWN finalized
- WAIT_DONE: 0xb9454dacf5228fa9767d4e4d0106a2dd727365e6c4b7a74dc9625a62d0bac32f status=UNKNOWN 
- WAIT_DONE: 0xb9454dacf5228fa9767d4e4d0106a2dd727365e6c4b7a74dc9625a62d0bac32f status=UNKNOWN 
- WAIT_DONE: 0xb9454dacf5228fa9767d4e4d0106a2dd727365e6c4b7a74dc9625a62d0bac32f status=UNKNOWN 
- PHASE: DEPLOY_FINALIZED
- PHASE: DEPLOY_DONE
- WAIT_START: 0x5d79d69c6148de8d9424b5355780de01ca9653dbe136989477c1b6f9cdafd659 status=UNKNOWN finalized
- WAIT_START: 0x5d79d69c6148de8d9424b5355780de01ca9653dbe136989477c1b6f9cdafd659 status=UNKNOWN finalized
- WAIT_START: 0x5d79d69c6148de8d9424b5355780de01ca9653dbe136989477c1b6f9cdafd659 status=UNKNOWN finalized
- WAIT_DONE: 0x5d79d69c6148de8d9424b5355780de01ca9653dbe136989477c1b6f9cdafd659 status=UNKNOWN 
- WAIT_DONE: 0x5d79d69c6148de8d9424b5355780de01ca9653dbe136989477c1b6f9cdafd659 status=UNKNOWN 
- WAIT_DONE: 0x5d79d69c6148de8d9424b5355780de01ca9653dbe136989477c1b6f9cdafd659 status=UNKNOWN 
- PHASE: OPEN_RECEIPT
- WAIT_START: 0xe1a24391d172f44ff497c1e7b8f37fef676e5984fdfe5c5b8662691a6bdc641d status=UNKNOWN finalized
- WAIT_START: 0xe1a24391d172f44ff497c1e7b8f37fef676e5984fdfe5c5b8662691a6bdc641d status=UNKNOWN finalized
- WAIT_START: 0xe1a24391d172f44ff497c1e7b8f37fef676e5984fdfe5c5b8662691a6bdc641d status=UNKNOWN finalized
- WAIT_DONE: 0xe1a24391d172f44ff497c1e7b8f37fef676e5984fdfe5c5b8662691a6bdc641d status=UNKNOWN 
- WAIT_DONE: 0xe1a24391d172f44ff497c1e7b8f37fef676e5984fdfe5c5b8662691a6bdc641d status=UNKNOWN 
- WAIT_DONE: 0xe1a24391d172f44ff497c1e7b8f37fef676e5984fdfe5c5b8662691a6bdc641d status=UNKNOWN 
- WAIT_START: 0xe20378d6e2f22c1cad42006a7bc637841af86c072838120094f9910b83df0b2c status=UNKNOWN finalized
- WAIT_START: 0xe20378d6e2f22c1cad42006a7bc637841af86c072838120094f9910b83df0b2c status=UNKNOWN finalized
- WAIT_START: 0xe20378d6e2f22c1cad42006a7bc637841af86c072838120094f9910b83df0b2c status=UNKNOWN finalized
- WAIT_DONE: 0xe20378d6e2f22c1cad42006a7bc637841af86c072838120094f9910b83df0b2c status=UNKNOWN 
- WAIT_DONE: 0xe20378d6e2f22c1cad42006a7bc637841af86c072838120094f9910b83df0b2c status=UNKNOWN 
- WAIT_DONE: 0xe20378d6e2f22c1cad42006a7bc637841af86c072838120094f9910b83df0b2c status=UNKNOWN 

## Resolve outcome (restricted enum and marker fields)
- STUDIO_RESOLVE_SAFE: status=none execution=none leader=SUCCESS vote=none
- STUDIO_RESOLVE_ERROR_MARKERS: 
- STUDIO_RESOLVE_VM_ERROR_COUNT: 0
- STUDIO_RESOLVE_SAFE_CASE_STATE: DECIDED
- STUDIO_PHASE5_IDLE_PROOF: RESOLVE agree=3 idle=2 synthetic_quorum_cancellations=2 fatal=0 unexplained_idle=0
- STUDIO_PHASE5_IDLE_PROOF: APPEAL agree=3 idle=2 synthetic_quorum_cancellations=2 fatal=0 unexplained_idle=0
- STUDIO_PHASE5_COMPLETE: RESOLVE_AND_APPEAL_TWO_IDLE_CAUSE_PROVEN
- PHASE4_READY: five validators, 2/2/1 conflicting responses
- PHASE4_DISAGREEMENT_START
- PHASE4_WAIT_RETURNED
- PHASE4_DISAGREEMENT_TX: 0xbc8c5a9616ebb75a07f0866f528936b31c02c8e084b35d8b79d83b26bb571351
- PHASE4_RECEIPT_KEYS: activator,appeal_validators_timeout,consensus_data,created_at,data,execution_mode,fees,from_address,gaslimit,hash,last_leader,last_round,leader_only,lifecycle,nonce,num_of_rounds,origin_address,recipient,result,result_name,sender,sim_config,to_address,triggered_on,txExecutionResult,txExecutionResultName,tx_id,type,value,value_credited
- PHASE4_RECEIPT_STATUS: UNKNOWN
- PHASE4_CONSENSUS_KEYS: leader_receipt,validators,votes
- PHASE4_VOTES: agree=0 disagree=3 idle=2 other=0
- PHASE4_CHAIN_STATE: state=OPEN decisions=0
- PHASE4_RPC_STATUS: FINALIZED
- PHASE4_HISTORY_ROUNDS: Undetermined
- PHASE4_ROTATION_COUNT: 0
- PHASE4_NO_SPARE_ROTATION: count=0 terminal=Undetermined
- PHASE4_ROLLBACK_STATE: OPEN decisions=0 case_unchanged=true
- PHASE4_RECOVERY_START
- PHASE4_RECOVERY_TX: 0x337de1d680bc9794813e526605db5f17452221821c3d4aff44327450a2a237f5
- PHASE4_RECOVERY_STATE: DECIDED decisions=1 outcome=VERIFIED
- PHASE4_COMPLETE: REAL_STUDIO_DISAGREEMENT_ROLLBACK_RECOVERY_PASS
- PHASE4_ROTATION_READY: five-member committee drawn from six validators with 2/2/2 conflicting responses
- PHASE4_DISAGREEMENT_START
- PHASE4_WAIT_RETURNED
- PHASE4_DISAGREEMENT_TX: 0xe1a24391d172f44ff497c1e7b8f37fef676e5984fdfe5c5b8662691a6bdc641d
- PHASE4_RECEIPT_KEYS: activator,appeal_validators_timeout,consensus_data,created_at,data,execution_mode,fees,from_address,gaslimit,hash,last_leader,last_round,leader_only,lifecycle,nonce,num_of_rounds,origin_address,recipient,result,result_name,sender,sim_config,to_address,triggered_on,txExecutionResult,txExecutionResultName,tx_id,type,value,value_credited
- PHASE4_RECEIPT_STATUS: UNKNOWN
- PHASE4_CONSENSUS_KEYS: leader_receipt,validators,votes
- PHASE4_VOTES: agree=2 disagree=3 idle=0 other=0
- PHASE4_CHAIN_STATE: state=OPEN decisions=0
- PHASE4_RPC_STATUS: FINALIZED
- PHASE4_HISTORY_ROUNDS: Leader Rotation,Undetermined
- PHASE4_ROTATION_COUNT: 1
- PHASE4_ROLLBACK_STATE: OPEN decisions=0 case_unchanged=true
- PHASE4_RECOVERY_START
- PHASE4_RECOVERY_TX: 0xe20378d6e2f22c1cad42006a7bc637841af86c072838120094f9910b83df0b2c
- PHASE4_RECOVERY_STATE: DECIDED decisions=1 outcome=VERIFIED
- PHASE4_ROTATION_COMPLETE: REAL_STUDIO_SPARE_VALIDATOR_ROTATION_ROLLBACK_RECOVERY_PASS
- STUDIO_SAFE_VOTE_COUNTS: agree=3 idle=2 unexpected=0
- STUDIO_PHASE5_IDLE_PROOF: RESOLVE agree=3 idle=2 synthetic_quorum_cancellations=2 fatal=0 unexplained_idle=0
- STUDIO_SAFE_APPEAL_VOTE_COUNTS: agree=3 idle=2 unexpected=0
- STUDIO_PHASE5_IDLE_PROOF: APPEAL agree=3 idle=2 synthetic_quorum_cancellations=2 fatal=0 unexplained_idle=0
- STUDIO_PHASE5_COMPLETE: RESOLVE_AND_APPEAL_TWO_IDLE_CAUSE_PROVEN
- STUDIO_SAFE_APPEAL_RESULT: state=APPEALED old=VERIFIED new=REJECTED decisions=2

## Local transaction state summaries
- TX_STATE|FINALIZED|count=12
- TX_DETAIL|FINALIZED|type=1|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=3
- TX_DETAIL|FINALIZED|type=2|mode=NORMAL|timestamp_missing=false|blocked=false|address_missing=false|count=9
- RESOLVE_CONSENSUS|status=FINALIZED|type=2|validator_entries=4|votes_type=object
- LIFECYCLE|total=12|finalized=12|unfinalized=0|write_calls=9

## Worker stages (counts only)
- WORKER_STAGE|finalization_started|count=12
- WORKER_STAGE|finalization_done|count=12
- WORKER_STAGE|finalization_not_ready|count=0
- WORKER_STAGE|finalization_accepted_repair|count=0
- WORKER_STAGE|finalization_error|count=0
- WORKER_STAGE|worker_task_failed|count=0
- WORKER_STAGE|worker_recovery|count=0
- WORKER_STAGE|worker_started|count=3

## Result
PASS
