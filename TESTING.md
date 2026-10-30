# Testing Notes

## Test command and environment
- GitHub Actions environment: Ubuntu 26.04; CPython 3.11.17; pytest 9.2.0.
- `python -m pip install -r requirements-dev.txt`: **passed**.
- `python -m pytest -q`: **247 passed in 0.21s**.
- `python -m main`: **passed**; output: `{'order_id': 'O-7', 'partner_id': 'P-2', 'pickup_minutes': 13, 'eta_minutes': 35, 'reason': 'assigned'}`.
- CI run: [Python tests — run #1](https://github.com/raohardik2805/SmartDispatch-Open-Source-Evaluation/actions/runs/41096247196) completed successfully. It checked out the branch, installed requirements, ran the complete pytest suite, and ran the demo.
- Baseline: not run before editing; no baseline count is claimed.

## Edge-case evidence

| # | Case / input | Expected behaviour | Actual result | Test name or evidence |
|---|---|---|---|---|
| 1 | Either required travel leg is absent | Candidate is ineligible; ETA is null | Pending automated run | Existing missing-route tests |
| 2 | Travel time is negative, boolean, string, NaN or infinity | Candidate is ineligible | Pending automated run | Existing acceptance matrix |
| 3 | Partner is inactive or at/over capacity | Partner is not selected | Pending automated run | Existing contract and capacity tests |
| 4 | Two eligible partners have equal ETA | Lexicographically smaller partner ID wins | Pending automated run | Existing tie-break tests |
| 5 | Same cancellation event is replayed | Workload is released once and event ID appears once | Pending automated run | Existing contract and cancellation matrix |
| 6 | Same event ID is replayed with a different order ID | Replay is ignored before changing the second order | Pending automated run | New changed-payload replay regression |
| 7 | Invalid capacity or non-boolean active flag | Partner is not selected | Pending automated run | New capacity and active-state regressions |

## Regression tests added
- Invalid time/workload values and malformed records.
- Invalid partner capacity and non-boolean active state.
- Cancellation replay with a changed payload.
- Input immutability for assignment and cancellation.

## Remaining failures or limitations
The GitHub Actions run passed all configured checks. This implementation is in-memory; it does not provide durable idempotency across process restarts or transactional updates across concurrent workers.
