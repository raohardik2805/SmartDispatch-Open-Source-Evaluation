# Challenges

## Challenge: cancellation event replay
A cancellation event may be delivered more than once. The starter removed an order if present and appended the event ID, but did not check whether that event ID had already been processed. Replay handling therefore depended only on whether the order happened to remain in the active-order list.

## Evidence from the starter
The original `process_cancellation` implementation unconditionally appended `event_id` after attempting to remove the order. The contract tests require a duplicate cancellation to leave workload at zero and record the event ID only once. The acceptance suite also exercises repeated event IDs and workload underflow boundaries.

## Investigation and resolution
- Inspected the original cancellation function and the contract/acceptance assertions.
- Added an early replay check against `processed_cancellation_ids`.
- The replay check occurs before order removal or workload adjustment, so a duplicate ID with a different order payload cannot release another order's workload.
- Kept the function non-mutating by working on a deep copy.

## Other edge conditions addressed
- Missing routes and invalid/non-finite time values make ETA estimates ineligible rather than being treated as zero.
- Candidate filtering rejects inactive partners and invalid/full capacity records.
- Invalid identifiers and malformed order/partner records fail closed.

## Verification and limitations
The regression suite passed in GitHub Actions: **247 passed**. The demo also exited successfully; exact output is recorded in `TESTING.md`. The implementation is in-memory and does not provide durable event storage or cross-process exactly-once guarantees; a production service would need persistent idempotency keys and transactional workload updates.
