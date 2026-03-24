# 300: Longest Increasing Subsequence

- **Difficulty:** Medium
- **Tags:** Array, Binary Search, Dynamic Programming
- **Pattern:** Tails array with structural domination

## Fundamentals

### Problem Contract
Given `nums`, return the length of the longest strictly increasing subsequence.

A subsequence preserves order but may skip elements.

### Definitions and State Model
Maintain an array `tails` where `tails[k]` is the minimum possible ending value among all increasing subsequences of length `k+1` seen so far.

The length of `tails` is the best LIS length known so far.

### Key Lemma / Invariant / Recurrence
#### Tails Invariant
After processing each prefix of `nums`:
- `tails` is strictly increasing,
- for every `k`, there exists an increasing subsequence of length `k+1` ending at `tails[k]`,
- and no increasing subsequence of length `k+1` seen so far can end with a value smaller than `tails[k]`.

#### Replacement Rule
When a new value `x` arrives, find the first index `p` with `tails[p] >= x`.
- If no such `p` exists, append `x`.
- Otherwise replace `tails[p]` by `x`.

Replacing is safe because a smaller tail is never worse for extending subsequences later.

### Algorithm
Process the array and binary-search the replacement position.

```text
tails = []
for x in nums:
    p = first index with tails[p] >= x
    if p == len(tails):
        tails.append(x)
    else:
        tails[p] = x
return len(tails)
```

### Correctness Proof
The tails invariant holds initially for the empty prefix.

Assume it holds before processing `x`. If `x` is larger than every element of `tails`, appending it extends the best known subsequence by one and preserves strict increase. Otherwise let `p` be the first index with `tails[p] >= x`. Then `p = 0` or `tails[p-1] < x <= tails[p]`. So `x` can terminate an increasing subsequence of length `p+1`, and replacing `tails[p]` by `x` preserves the existence of such a subsequence while making its tail no larger. That preserves the minimal-tail property.

Because `tails[k]` records the minimal possible tail for length `k+1`, the array length can increase only when a truly longer increasing subsequence is found. Conversely, every increasing subsequence of length `L` forces `tails` to have length at least `L` after its last element is processed. Therefore `len(tails)` equals the LIS length.

### Complexity Analysis
Let `n = len(nums)`.

- The loop processes each value once.
- Each step performs one binary search on `tails`, whose length is at most `n`.

The running time is `O(n log n)`. The auxiliary space is `O(n)` for `tails`.

## Appendix

### Common Pitfalls
- `tails` does not itself have to be a subsequence of the original array; it is a summary structure for proof and search.
- Using `>` instead of `>=` in the binary search computes a nondecreasing subsequence length instead of a strictly increasing one.
