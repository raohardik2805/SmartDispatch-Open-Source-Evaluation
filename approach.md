# Approach

## Baseline
- The starter test suite was inspected before changes, but a baseline run was not available in this environment.
- The GitHub connector can read and write repository content but does not provide a local Python shell. A local clone attempt failed because outbound DNS/network access was unavailable.
- No baseline pass/fail count is claimed.

## Codebase understanding
- `service.py` contains ETA estimation, candidate selection, and cancellation handling.
- `models.py` defines the order and partner dictionaries used by the service.
- `fixtures.py` supplies the offline demo inputs; `main.py` calls `assign_order`.
- Acceptance tests specify the ETA formula, strict partner eligibility, capacity boundaries, deterministic tie-breaking, and cancellation replay behaviour.

## Implementation strategy
- Centralized finite, non-negative numeric validation in `_valid_minutes`; booleans, strings, negative values, NaN, infinity, and oversized integers are rejected.
- Made ETA estimation fail closed when identifiers, required travel legs, preparation time, current time, or workload are invalid.
- Filtered dispatch candidates to partners whose `active` field is exactly `True`, whose capacity is a positive integer, and whose active-order count is below capacity.
- Kept selection deterministic by comparing ETA and partner ID.
- Made cancellation replay-safe by checking an event ID before mutating workload, while retaining deep-copy behaviour.

## Verification
- Added focused regression tests in `tests/test_validation_regressions.py`.
- The repository's GitHub Actions workflow runs the demo and visible pytest suite on pull requests. Results will be recorded in `TESTING.md` when available.
- No local test result or performance measurement is claimed.
