# 42: Trapping Rain Water

- **Difficulty:** Hard
- **Tags:** Array, Two Pointers, Dynamic Programming
- **Pattern:** Two-pointer scan with maintained maxima

## Fundamentals

### Problem Contract
Given `height[0..n-1]`, interpret `height[i]` as the wall height at index `i`. Return the total water trapped after rain.

For each index `i`, the trapped water is determined by the lower of the highest wall to its left and the highest wall to its right:
```text
water(i) = max(0, min(left_max(i), right_max(i)) - height[i]).
```
The objective is
```text
sum water(i) over all indices i.
```

### Definitions and State Model
Maintain two pointers `l` and `r`, together with
- `left_max = max(height[0..l])`,
- `right_max = max(height[r..n-1])`,
- `ans =` total water already finalized.

The unprocessed region is `[l, r]`. The algorithm will finalize exactly one side per iteration.

### Key Lemma / Invariant / Recurrence
#### Finalization Lemma
If `left_max <= right_max`, then the water above index `l` is already determined by `left_max` alone:
```text
water(l) = max(0, left_max - height[l]).
```
The reason is that every future right boundary is at least `right_max`, so the smaller boundary in `min(left_max, right_max)` is fixed at `left_max`. The symmetric statement holds when `right_max < left_max`.

#### Scan Invariant
Before each iteration, `ans` equals the total water for every index strictly outside `[l, r]`, and `left_max` and `right_max` are correct maxima for their processed sides.

### Algorithm
1. Initialize `l = 0`, `r = n - 1`, `left_max = 0`, `right_max = 0`, `ans = 0`.
2. Update `left_max` with `height[l]` and `right_max` with `height[r]`.
3. If `left_max <= right_max`, finalize index `l` using `left_max` and increment `l`.
4. Otherwise finalize index `r` using `right_max` and decrement `r`.
5. Repeat until `l > r`.

```text
l = 0
r = n - 1
left_max = 0
right_max = 0
ans = 0

while l <= r:
    left_max = max(left_max, height[l])
    right_max = max(right_max, height[r])
    if left_max <= right_max:
        ans += left_max - height[l]
        l += 1
    else:
        ans += right_max - height[r]
        r -= 1
return ans
```

### Correctness Proof
Initially no index is finalized, so the scan invariant holds with `ans = 0`.

Assume the invariant holds at the start of an iteration. If `left_max <= right_max`, the finalization lemma shows that the trapped water at `l` depends only on `left_max`; future movement of `r` cannot reduce the right boundary below `right_max`, so the contribution of `l` is fixed. Adding `left_max - height[l]` if positive, then incrementing `l`, preserves the invariant because the finalized set grows by one correct index. The case `right_max < left_max` is symmetric for index `r`.

The loop terminates after every index has been finalized exactly once. By the invariant, `ans` then equals the sum of correct contributions over all indices, so the algorithm returns the total trapped water.

### Complexity Analysis
Let `n = len(height)`.

- Each iteration moves exactly one pointer inward.
- Each pointer moves at most `n` times.
- The work per iteration is `O(1)`.

Therefore the running time is `O(n)` and the auxiliary space is `O(1)`.

## Appendix

### Common Pitfalls
- Finalizing `l` because `height[l] <= height[r]` is weaker than the correct rule; the proof depends on comparing `left_max` and `right_max`, not the raw endpoint heights.
- Precomputing left and right maxima arrays is correct, but it changes the space bound from `O(1)` to `O(n)`.
