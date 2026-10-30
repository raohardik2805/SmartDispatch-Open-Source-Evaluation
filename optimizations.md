# Optimizations

## Objective
The primary objective was correctness and predictable behaviour at input boundaries, not raw speed. The starter was small, and no benchmark evidence justified a more complex dispatch data structure.

## Changes implemented
- Added a shared numeric-validation helper to avoid repeating slightly different checks for each time input.
- Used a single candidate list and deterministic `min` key for dispatch selection. This keeps the implementation easy to inspect and has linear candidate-selection cost.
- Kept cancellation state updates on a deep copy to avoid surprising mutation of caller-owned partner data.

## Options considered
- Sorting every candidate before choosing one would add work without changing the selected result; a single `min` pass is simpler.
- Introducing classes or a validation framework would add abstraction disproportionate to this small dictionary-based exercise.
- Replacing the cancellation ID list with a set could improve membership lookup for large histories, but would change the current list-shaped data contract. A persistent indexed store would be a better production-level solution.

## Measurements and trade-offs
No performance benchmark was run, so no speedup is claimed. Validation adds a small amount of work per candidate but prevents invalid time data from producing unreliable ETAs. Deep-copy cancellation handling uses additional memory, in exchange for preserving the input object.

## Further improvements
For a larger dispatch service, consider typed models, persistent idempotency keys, transactional workload accounting, and benchmarks over realistic partner counts. These changes should be introduced only with corresponding contract tests and measured evidence.
