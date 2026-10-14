# ConsensusGuard — Studio Dev non-GenVM contract and explorer read-only fallback

Official Studio source: local tag v0.123.0-rc.7, endpoint implementations.
CI https://github.com/maho0638/consensusguard-genlayer/actions/runs/38574091907
No wallet secrets, no wallet signature, no GEN spending or transactions.

- RPC_contract_code: text len=33304, available=true
- RPC_contract_nonce: result type=int
- RPC_transactions_for_contract: list length=4
  - transaction groups: {"1 / FINALIZED": 1, "2 / FINALIZED": 3}
  - inspection_note: no actual appeal submitted can be assumed from txn count alone
- RPC_transactions_for_contract_proxy: list length=4
  - transaction groups: {"1 / FINALIZED": 1, "2 / FINALIZED": 3}
  - inspection_note: no actual appeal submitted can be assumed from txn count alone
- RPC_historical_complete: result type=dict, field_count=41
- RPC_historical_finalization: text len=9, available=true
- Explorer_address: json OK, contract_type=CONTRACT, transaction_payload_count=4
  - recent tx classes: {"1/FINALIZED": 1, "2/FINALIZED": 3}
- Explorer_contract: error=HTTPError http_code=404
- Explorer_tx_page: json OK, contract_type=unknown, transaction_payload_count=4
  - recent tx classes: {"1/FINALIZED": 1, "2/FINALIZED": 3}
- Explorer_proxy_contract: error=HTTPError http_code=404
- Studio_server_contract: json OK, contract_type=CONTRACT, transaction_payload_count=4
  - recent tx classes: {"1/FINALIZED": 1, "2/FINALIZED": 3}

## How to interpret
The original contract-level appeal is not proven until a signed original-requester transaction is FINALIZED
and the smart-contract state and both decisions are read back. An explorer transaction listing alone
cannot prove app-level state. A local Studio result is not a live Studio Dev result.
