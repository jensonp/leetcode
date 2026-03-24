# 55: Jump Game

- **Difficulty:** Medium
- **Tags:** Array, Greedy
- **Pattern:** Prefix reachability invariant

## Fundamentals

### Problem Contract
Given `nums[0..n-1]` with nonnegative jump lengths, start at index `0`. From index `i`, one move may land at any index in `[i+1, i+nums[i]]`. Return whether index `n-1` is reachable.

The problem is feasibility, not minimum jump count.

### Definitions and State Model
Define `farthest` as the maximum index reachable from some path that starts at `0` and uses only processed indices. After scanning prefix `0..i`, the maintained state is
```text
farthest = max(j + nums[j]) over reachable j in [0, i].
```

### Key Lemma / Invariant / Recurrence
#### Prefix Reachability Invariant
At the start of iteration `i`, every index in `[0, farthest]` is reachable, and no index greater than `farthest` has yet been proved reachable.

#### Failure Lemma
If `i > farthest`, then index `i` is unreachable. Since every future path must pass through some earlier reachable index, no later index can be reached either, and the answer is immediately `false`.

### Algorithm
Scan from left to right while maintaining `farthest`.

```text
farthest = 0
for i in 0 .. n-1:
    if i > farthest:
        return false
    farthest = max(farthest, i + nums[i])
    if farthest >= n - 1:
        return true
return true
```

### Correctness Proof
Initially `farthest = 0`, so the prefix reachability invariant holds: only index `0` is known reachable.

Assume the invariant holds at iteration `i`. If `i > farthest`, the failure lemma applies, so returning `false` is correct. Otherwise `i` is reachable. From `i`, the jump rule makes every index up to `i + nums[i]` reachable as well, so updating `farthest` to `max(farthest, i + nums[i])` preserves the invariant.

If the algorithm returns `true` because `farthest >= n-1`, then the last index is reachable by definition of `farthest`. If the loop finishes without failure, every scanned index was reachable, including `n-1`, so returning `true` is correct. Therefore the algorithm returns `true` exactly when the end is reachable.

### Complexity Analysis
Let `n = len(nums)`.

- The loop visits each index once.
- Each iteration performs `O(1)` work.

The running time is `O(n)` and the auxiliary space is `O(1)`.

## Appendix

### Common Pitfalls
- Treating this as dynamic programming is correct but unnecessary; the greedy prefix invariant already captures all reachable states.
- Returning `false` only after the full scan misses the early-failure proof at the first `i > farthest`.
