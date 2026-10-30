# Testing Notes

## Test command and environment
- Python version: Not available in the current connector-only execution environment.
- Required commands: `python -m pip install -r requirements-dev.txt`, `python -m pytest -q`, `python -m main`.
- Actual test summary: Not yet available. The repository's GitHub Actions workflow runs these checks on pull requests. Results will be added after the workflow completes.
- Baseline: Not run before editing; no baseline count is claimed.

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
Automated results are pending. This implementation is in-memory; it does not provide durable idempotency across process restarts or transactional updates across concurrent workers.
