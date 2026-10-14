# 2026-10-14 Studio Dev RPC diagnostic — all read only

CI: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38572274052
Studio Dev canonical RPC chain expected: 61997. No writes, wallet, test GEN or contract deploy.

## Safe observations
- chain_identity: expected_chain_id_61997=True
- historical_transaction: found=True; status=FINALIZED
- contract_storage_finalized: ERROR code=-32601 msg=Method not found: gen_getContractState
- contract_storage_accepted: ERROR code=-32601 msg=Method not found: gen_getContractState
- contract_schema_finalized: ERROR code=-32603 msg=(psycopg2.ProgrammingError) can't adapt type 'dict' [SQL: SELECT current_state.id AS current_state_id, current_state.data AS current_state_data, current_state.balance AS current_st
- explorer_historical_transaction: found=True
