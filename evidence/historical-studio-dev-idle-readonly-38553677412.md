# Phase 5 — 2026-10-12 historical Studio Dev transaction, read-only retrieval

Historical transaction: \`0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9\`
Studio Dev (NOT localnet), documented chain ID: 61997
GitHub CI: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38553677412
No wallet, faucet, deploy, GenVM execution or write operation was used.
Only whitelisted known transaction lookups; raw RPC responses and node configs are never printed or stored.

## Endpoint diagnostics
- studio-dev official RPC eth_getTransactionByHash: full consensus record located; agree=3 idle=2; matched receipts=2; proven benign quorum cancellation=2; unmatched=0
- studio-dev official RPC gen_getTransactionReceipt: RPC error code -32601 (message intentionally redacted)
- studio-dev explorer backend transaction: full consensus record located; agree=3 idle=2; matched receipts=2; proven benign quorum cancellation=2; unmatched=0
- studio-dev explorer RPC proxy eth_getTransactionByHash: full consensus record located; agree=3 idle=2; matched receipts=2; proven benign quorum cancellation=2; unmatched=0

## Historical decision
**VERIFIED: both historical Studio Dev IDLE records explicitly carry nonfatal quorum cancellation causes.**
The local five-validator tests are separately proven and are not substituted for the historical receipt.
Historical preview state may be reset or RPC/explorer access may be restricted; these conditions do not prove the old validator causes.
For a definitive historic diagnosis if inaccessible, retrieve/export the original transaction's full JSON from the Studio Dev explorer or server-side historical archive and verify both receipts.
