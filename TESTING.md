# Testing Notes

## Test command and environment
- Python version used for local validation: 3.13.5; pytest 9.0.2.
- `python -m pip install -r requirements-dev.txt`: completed successfully (pytest was already installed and satisfied the requirement).
- `python -m pytest -q`: **247 passed in 0.23s**.
- `python -m main`: exited 0 and printed `{'order_id': 'O-7', 'partner_id': 'P-2', 'pickup_minutes': 13, 'eta_minutes': 35, 'reason': 'assigned'}`.
- Execution note: outbound DNS prevented a direct `git clone`, so the local test workspace was assembled from the branch's fetched source files and test modules. The test modules were recreated from the fetched repository contents; this is local validation of the fetched branch code, not a GitHub-hosted Actions run. The added GitHub Actions workflow has not yet produced a visible run.
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
GitHub-hosted CI remains pending even though the local fetched-source test run passed. This implementation is in-memory; it does not provide durable idempotency across process restarts or transactional updates across concurrent workers.
