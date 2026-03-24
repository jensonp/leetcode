# 198: House Robber

- **Difficulty:** Medium
- **Tags:** Array, Dynamic Programming
- **Pattern:** 1D recurrence with adjacent-exclusion choice

## Fundamentals

### Problem Contract
Given nonnegative values `nums[0..n-1]`, choose a subset of indices with no adjacent pair and maximize the sum of chosen values.

### Definitions and State Model
Let `dp[i]` denote the maximum amount obtainable from the prefix `nums[0..i]`.

At index `i`, there are exactly two legal choices:
- skip `i`, keeping `dp[i-1]`,
- take `i`, forcing index `i-1` to be absent and yielding `nums[i] + dp[i-2]`.

### Key Lemma / Invariant / Recurrence
#### Recurrence
For `i >= 2`,
```text
dp[i] = max(dp[i-1], nums[i] + dp[i-2]).
```
This is exhaustive because every optimal solution either includes `i` or excludes `i`, and these cases are mutually exclusive.

### Algorithm
Use rolling variables for the recurrence.

```text
if n == 0: return 0
if n == 1: return nums[0]
prev2 = nums[0]
prev1 = max(nums[0], nums[1])
for i in 2 .. n-1:
    cur = max(prev1, nums[i] + prev2)
    prev2 = prev1
    prev1 = cur
return prev1
```

### Correctness Proof
The base cases are correct: the best value for one house is `nums[0]`, and for two houses it is `max(nums[0], nums[1])`.

Assume the recurrence value is correct for all smaller indices. For prefix `0..i`, any feasible solution either skips house `i` or takes it. If it skips `i`, its value is at most `dp[i-1]`. If it takes `i`, then `i-1` cannot be used, so its value is at most `nums[i] + dp[i-2]`. Taking the maximum of these two cases gives the optimal value for `dp[i]`.

The rolling implementation stores exactly the last two recurrence values, so by induction it returns the optimal total for the full array.

### Complexity Analysis
Let `n = len(nums)`.

- The loop visits each index once.
- Each iteration does `O(1)` arithmetic.

The running time is `O(n)`. The rolling-state implementation uses `O(1)` auxiliary space.

## Appendix

### Common Pitfalls
- Greedily taking the locally larger of two adjacent houses fails because the effect of a choice extends beyond one step.
- Using `prev2 = 0, prev1 = 0` is valid, but the update order must preserve the old `prev1` value before overwriting it.
