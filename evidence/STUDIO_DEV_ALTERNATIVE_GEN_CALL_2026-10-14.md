# Alternate GenLayer execution RPC — original requester address; read-only

CI https://github.com/maho0638/consensusguard-genlayer/actions/runs/38574439443
Original sender pulled from finalized transaction; no account identity or private key logged.
All type=read operations, no chain writes.

- gen_call_original_sender_latest_final: RPC_ERROR code=-32603 category=SQLALCHEMY_UNROLLED_BACK_CONNECTION
- gen_call_original_sender_status_finalized: RPC_ERROR code=-32603 category=SQLALCHEMY_UNROLLED_BACK_CONNECTION
- sim_call_original_sender_status_finalized: RPC_ERROR code=-32603 category=SQLALCHEMY_UNROLLED_BACK_CONNECTION
- eth_call_original_sender_finalized: RPC_ERROR code=-32603 category=SQLALCHEMY_UNROLLED_BACK_CONNECTION
- explorer_rpc_proxy_gen_call: RPC_ERROR code=-32603 category=SQLALCHEMY_UNROLLED_BACK_CONNECTION
- explorer_rpc_proxy_sim_call: RPC_ERROR code=-32603 category=SQLALCHEMY_UNROLLED_BACK_CONNECTION

CONTRACT-LEVEL APPEAL PROVEN? **NO** — only case-state inspection attempted.
