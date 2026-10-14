# Studio Dev original deployed-code comparison and signed appeal preparation

Run: https://github.com/maho0638/consensusguard-genlayer/actions/runs/38574091907

All checks here are GET/JSON-RPC read-only; no wallet, GEN spend or transactions.

## Pre-computed manifest
- Valid manifest entries: 2, normalized hosts distinct, lowercase SHA-256 exact.
- Earlier case manifest SHA-256: \`84f349ded38dfd428b3c83f35756bb4d1699ee90850a80e6f6f3577e8cd6fede\`
- Proposed new normalized manifest SHA-256: \`35dfb62ffa565d9679256baa75278162c82448f4c949829d10499738339bfd18\`
- Manifest reorder only: prior source texts and statuses remain unchanged; demonstrates case lifecycle only.
- Original test wallet signature is mandatory; requester-only contract authorization cannot be bypassed.

```json
[{"url":"https://httpbingo.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQiBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu","sha256":"1ae8c7be8b2c578b9b8b04130a4e62b6f96288fd30deb08aa2d5c5f81d056ece"},{"url":"https://httpbin.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQSBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu","sha256":"86ac284424d831f8799457c075295ea59bafb0c9a0d034e8859979b4a82e1609"}]
```

## Independent source HTTP retrieval
- source 1: HTTP byte integrity PASS, bytes=66
- source 2: HTTP byte integrity PASS, bytes=66

## Historical deployed code
- Studio Dev deployed code fetch unavailable: HTTPError

## Signer and network boundary
1. The smart contract is requester-only and *only* the account that opened case 0 can sign a valid \`appeal\`.
2. The Studio Dev read RPC currently returns SQLAlchemy pending-rollback errors.
3. An appeal must not be represented as complete unless the transaction is \`FINALIZED\` and decisions are read back.
4. Do not submit the prepared manifest automatically, do not expose private keys or wallet recovery phrases.
