# Dispatch Notes

## 1. Worked ETA example
Using the offline fixture in `fixtures.py`:
- Order: `O-7`; restaurant `R-2`; destination `Z-9`; preparation = 10 minutes.
- Partner `P-2` is in `Z-1`, has 5 minutes of remaining workload, and has 1 active order.
- Partner-to-restaurant travel = 8 minutes; restaurant-to-destination travel = 12 minutes.
- Pickup time = current time 0 + 8 + 5 = **13 minutes**.
- Delivery ETA = 13 + 10 + 12 = **35 minutes**.
- Partner `P-1` has no route from `Z-3` to `R-2`, so that candidate is ineligible rather than receiving a zero-minute route.
- Observed GitHub Actions demo output: `{'order_id': 'O-7', 'partner_id': 'P-2', 'pickup_minutes': 13, 'eta_minutes': 35, 'reason': 'assigned'}`; the command exited successfully.

## 2. No-eligible-partner example
For an order from restaurant `R` to destination `D`, suppose the only active partner is already at capacity and a second partner has no `(zone, R)` travel entry. The first candidate fails the capacity filter; the second cannot receive a reliable ETA. The service returns an unassigned result with null ETA and a reason explaining that no eligible partner or required time data was available.

## 3. Three edge cases
1. **Missing route:** if either route leg is absent, ETA is null and the candidate is ineligible. Covered by existing missing-route tests; automated result pending.
2. **Invalid time:** negative, boolean, string, NaN, or infinite travel/preparation/workload/current-time values are rejected. Covered by acceptance and new regression tests; automated result pending.
3. **Duplicate cancellation:** replaying an already processed event ID does not remove another order or decrement workload again. Covered by the contract test and new changed-payload regression; automated result pending.

## 4. Assumptions and limitations
- ETA = current time + partner-to-restaurant travel + remaining partner workload + restaurant preparation + restaurant-to-customer travel.
- Lowest ETA wins; exact ties use ascending lexicographic partner ID.
- Only explicitly active partners with a positive integer capacity and spare slots are candidates.
- Cancellation event IDs are idempotency keys within the in-memory partner record. Durable or concurrent exactly-once handling requires persistent transactional storage.
