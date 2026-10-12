# Studio Dev live validation record

Date: 2026-10-12 (Studio UI timestamps are UTC). This run used Studio Dev,
contract `contracts/consensus_guard.py`, runner
`py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng`, and
**Normal (Full Consensus)** mode. The wallet UI rounded its displayed balance
to `0 GEN`. Explorer transaction details show a fee of approximately
`0.000097 GEN`; the exact debit/refund values are included in the browser
record. This was test-wallet activity on Studio Dev, not mainnet.

## Deployment and writes

| Action | Transaction / status | Result |
|---|---|---|
| Deploy | `0x904e5c999136fe7d0e804b851a293e301d9347283f001ebea14cb0e996159012` — `FINALIZED` | Studio log: `Reached consensus`, `Contract deployed`. Address: `0xBa84783D71d902c8BD3Ba63418Df172280249139`. |
| First `open_case` attempt | `0x797a26bf2007e4e97aab27e6c6af708ce23ee65eda48bfb2baec54f5118cae36` — `FINALIZED` | **Failed contract execution:** `USER_ERROR: duplicate source host`. Both URLs used `httpbin.org`. This is recorded as a failed attempt, not a passing test. |
| Corrected `open_case` | `0x00ac7f88f17cd4f22cab60d06e6d56cb39843f651681a8c3ddaac8f742327dd3` — `FINALIZED` | Distinct URL hostnames (`httpbin.org`, `httpbingo.org`); later read returned `case_count = 1`. |
| `resolve(0)` | `0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9` — `FINALIZED` | In Full Consensus mode. Explorer shows `Initial Validators: 5`, `Validators: 5`, and `Consensus Result: Accepted`; the transaction reached `FINALIZED`. The consensus vote map has three `agree` and two `idle` entries. Validator identities are not reproduced here. |

## Contract read-back

Studio Run and Debug read calls returned `case_count = 1` and
`decision_count = 1`. `get_latest_decision(0)` and `get_case(0)` returned the
following decision record (JSON copied from the UI response):

```json
{
  "author": "[redacted requester address]",
  "case_id": 0,
  "decided_at": "2026-10-12T20:49:36.240498+00:00",
  "id": 0,
  "manifest_sha256": "84f349ded38dfd428b3c83f35756bb4d1699ee90850a80e6f6f3577e8cd6fede",
  "outcome": "VERIFIED",
  "policy_sha256": "db5cb6f2471495ec282a9dad3ff9f1435cf82d6197517642d8d77022731c2b80",
  "reason_code": "SUPPORT_THRESHOLD_MET",
  "refute_count": 0,
  "round": 0,
  "source_results": [
    {
      "expected_sha256": "86ac284424d831f8799457c075295ea59bafb0c9a0d034e8859979b4a82e1609",
      "index": 0,
      "integrity": "VERIFIED",
      "label": "SUPPORTS",
      "observed_sha256": "86ac284424d831f8799457c075295ea59bafb0c9a0d034e8859979b4a82e1609",
      "url": "https://httpbin.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQSBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu"
    },
    {
      "expected_sha256": "1ae8c7be8b2c578b9b8b04130a4e62b6f96288fd30deb08aa2d5c5f81d056ece",
      "index": 1,
      "integrity": "VERIFIED",
      "label": "SUPPORTS",
      "observed_sha256": "1ae8c7be8b2c578b9b8b04130a4e62b6f96288fd30deb08aa2d5c5f81d056ece",
      "url": "https://httpbingo.org/base64/Q29uc2Vuc3VzR3VhcmQgdGVzdCBzb3VyY2UgQiBzYXlzIENPTlNFTlNVU0dVQVJEX1RFU1RfU1RBVFVTPVBBU1Mu"
    }
  ],
  "support_count": 2,
  "unclear_count": 0,
  "verified_count": 2
}
```

The requester wallet address is redacted from the package; all other decision
fields above are copied from the Studio response.

The bodies were synthetic deterministic test fixtures returned by Base64
endpoints. Both contained the committed `CONSENSUSGUARD_TEST_STATUS=PASS`
token, and their observed body hashes matched. Different hostnames here are
only an input-validation/test fixture; this result does **not** establish
independent publishers, source ownership, or the truth of any external claim.
The result demonstrates that this Studio Dev transaction reached consensus
and stored the contract's expected result for this controlled case. The UI
shows five initial validators and five validator slots. The separate `votes`
map has three `agree` and two `idle` entries; detailed validator result
records include two idle execution errors and two agree executions, with the
leader receipt recorded separately. These fields must not be simplified to
“five successful independent executions.” The accepted transaction was
finalized and the contract read-back matched the stored decision.

## Local regression suite after Studio run

After the Studio run, the full local suite was repeated:

```text
66 passed, 1 skipped in 2.82s
SKIPPED tests/test_studio_multivalidator.py: set CONSENSUSGUARD_RUN_STUDIO=1 to run against local GenLayer Studio
```

The skipped test is the separate **local five-validator harness**; this does
not negate or replace the live Studio Dev transaction above. The Studio
transaction was executed in the browser and is not represented as a passing
local integration test. Other post-run checks passed: compileall, 3 GenVM AST
lint checks, pinned-SDK schema extraction (8 public methods), Pyright (0
diagnostics), `pip check`, and pinned runner/SDK archive SHA-256 verification.
The fee evidence above supersedes the earlier wallet-UI-only observation of no
visible debit. Explorer shows an approximate total fee of 0.000097 GEN.
