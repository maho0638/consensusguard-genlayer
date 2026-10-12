# GLSim forced-dissent and rollback investigation

## Historical failed experiment

The first exploratory hook forced disagreement only during the first two of
three configured rotations. It stopped injecting dissent before the third
rotation, where GLSim finalized. The exact recorded result was:

```text
assert consensus.status.value == "UNDETERMINED"
AssertionError: assert 'FINALIZED' == 'UNDETERMINED'
VOTE CALLS [1, 1] TxStatus.FINALIZED ['agree', 'agree', 'agree', 'agree', 'agree'] 2
```

This was a flawed probe and is not a passing result. It did not test persistent
disagreement or establish rollback.

## Follow-up diagnosis and correction

The GLSim package's `run_consensus` clears captured validators per rotation,
calls validator callbacks when present, and restores storage snapshots after a
non-majority. The local GenLayer v0.3 storage adapter also caches a root slot on
the contract instance. Restoring the in-memory manager alone left the next
rotated execution attached to a stale slot, so the next `resolve` saw `DECIDED`
and failed with `case is not open`.

The test harness now rebuilds the contract's storage descriptor against the
restored manager after a failed rotation. This is a local GLSim/test-adapter
compatibility shim; it does not change contract runtime code. The corrected
`test_glsim_contract_disagreement_does_not_store_decision` keeps all five
validators in dissent for all three rotations and asserts `UNDETERMINED`,
`OPEN`, and zero decisions. It passes. A separate synthetic test exercises the
simulator's snapshot restore in isolation. The ordinary GLSim contract test
also asserts that a validator callback was captured and replayed for the
agreement case.

Current limits: these are single-process GLSim tests using the local adapter.
They do not prove independent Studio validator processes or real-chain
transaction rollback. The opt-in Studio test remains unrun because a local
Studio node and network/socket access are unavailable.
