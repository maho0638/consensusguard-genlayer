# State machine

## Case states

| Current state | Operation | Caller | Next state | Effect |
|---|---|---|---|---|
| — | `open_case` | Any address | `OPEN` | Stores fixed claim, criteria, source manifest, threshold, and requester. |
| `OPEN` | `resolve` | Original requester only | `DECIDED` | Appends round 0 only after accepted validator consensus and evidence threshold handling. |
| `DECIDED` | `appeal` | Original requester only | `APPEALED` | Accepts one new manifest and appends round 1 only after consensus. |
| `DECIDED` | `resolve` | Original requester only | Revert | Duplicate resolution blocked. |
| `APPEALED` | `resolve` or `appeal` | Original requester only | Revert | No repeat evaluation or second appeal. |

## Revert and no-write cases

- Invalid input, duplicate key, nonexistent ID, unauthorized appeal, malformed model output, or invalid classifier labels revert before decision append.
- A failed or undetermined GenLayer consensus does not write case state or decision state.
- Retrying `resolve` is allowed only while the case remains `OPEN`.
- Whenever fewer than `min_valid_sources` entries pass integrity checks, classification is skipped. If one or more fetches are policy-classified `UNAVAILABLE` (transport/DNS exception, HTTP 408/425/429 or 5xx), `resolve` reverts before append; the case stays `OPEN` and the requester may retry. “Retryable” does not mean the contract knows the fault is temporary.
- Other returned non-2xx statuses are `HTTP_ERROR` for that attempt; this does not prove the error is permanent. If the evidence threshold is not met, the agreed result is terminal `INCONCLUSIVE` for the round; the requester can use the one appeal to submit a corrected manifest. Available sources with bad hash/size/encoding follow the same terminal path.
- Retrying an appeal is allowed only if the appeal transaction did not reach a successful state change. Once round 1 is recorded, another appeal reverts.

## Decision history

`DecisionRecord` entries are append-only and contain the case ID, round, author, outcome, reason code, policy digest, manifest digest, ordered source observations, counts, and deterministic transaction timestamp. An appeal changes the case's current state and latest-decision pointer but leaves prior decision records intact.
