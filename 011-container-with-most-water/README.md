# 11: Container With Most Water

- **Difficulty:** Medium
- **Tags:** Array, Two Pointers, Greedy
- **Pattern:** Two-pointer state-space pruning

## Fundamentals

### Problem Contract
Given a non-negative array `height[0..n-1]`, define
```math
A(i,j) = (j-i)\min(H[i], H[j]), \qquad 0 \le i < j < n.
```
Return
```math
\max_{0 \le i < j < n} A(i,j).
```

The contract has four consequences that the solution depends on:
- For a fixed pair `(i, j)`, only the endpoints `i` and `j` affect `A(i, j)`. Interior lines do not change the area of that candidate container.
- If `H[i] <= H[j]`, then `H[i]` is the bottleneck height for `A(i, j)`. Changing only `H[j]` cannot increase the area of that same pair.
- Width is tied to the original indices. Sorting the heights destroys the distances that define the objective.
- All heights are non-negative, so all candidate areas are non-negative.

### Definitions and State Model
Let `H` be the height array, and let
```math
S = \{(x,y) \mid 0 \le x < y < n\}
```
be the search space of valid pairs.

For each `(i, j) \in S`, define
```math
A(i,j) = (j-i)\min(H[i], H[j]).
```
This is the exact objective being maximized.

The algorithm maintains two pointers `i` and `j` with `0 <= i < j < n`, together with a value `best` equal to the largest area already seen. The active search window is the index interval `[i, j]`.

### Key Lemma / Invariant / Recurrence
#### Pruning Lemma
If `H[i] <= H[j]`, then for every `k` with `i < k < j`,
```math
A(i,k) = (k-i)\min(H[i], H[k])
       \le (k-i)H[i]
       < (j-i)H[i]
       \le (j-i)\min(H[i], H[j])
       = A(i,j).
```
Therefore, once `(i, j)` has been evaluated and `H[i] <= H[j]`, index `i` can be discarded permanently. The case `H[j] <= H[i]` is symmetric.

#### Search Invariant
At the start of each iteration, either:
- `best` already equals the global optimum, or
- some optimal pair lies entirely inside the current window `[i, j]`.

The correctness proof will show that the pruning lemma preserves this invariant.

### Algorithm
Start with `(i, j) = (0, n - 1)` and update the pointers by the sign of `H[i] - H[j]`:

1. Initialize `i = 0`, `j = n - 1`, and `best = 0`.
2. Evaluate `A(i, j)` and update `best`.
3. If `H[i] <= H[j]`, increment `i`; otherwise, decrement `j`.
4. Repeat until `i == j`.

Pseudocode:

```text
i = 0
j = n - 1
best = 0

while i < j:
    best = max(best, (j - i) * min(H[i], H[j]))
    if H[i] <= H[j]:
        i += 1
    else:
        j -= 1

return best
```

The only nontrivial step is the pointer move in Step 3. Its validity is exactly the pruning lemma above.

### Correctness Proof
We prove that the algorithm returns the maximum area.

**Initialization.** Initially `i = 0` and `j = n - 1`, so the active window contains every valid pair in `S`. The search invariant therefore holds.

**Maintenance.** Assume the invariant holds at the start of an iteration with pointers `(i, j)`.

- If `H[i] <= H[j]`, the pruning lemma shows that every discarded pair `(i, k)` with `i < k < j` is strictly worse than the already evaluated pair `(i, j)`. Since `best` is updated with `A(i, j)` before the move, incrementing `i` cannot discard a pair that improves on `best`.
- If `H[j] <= H[i]`, the symmetric argument shows that every discarded pair `(k, j)` is strictly worse than `(i, j)`, so decrementing `j` is equally safe.

Thus, after applying the update dictated by `H[i]` and `H[j]`, the search invariant still holds.

**Termination.** The loop stops when `i == j`. At that point no valid pair remains in the window. By the invariant, every optimal pair has either already been evaluated or has been safely dominated by a pair whose value was recorded in `best`. Therefore `best` is the maximum area.

### Complexity Analysis
Let `n` be the length of `height`.

- Each iteration performs `O(1)` work: one subtraction, one `min`, one multiplication, one `max`, and one pointer move.
- At each iteration exactly one pointer moves inward, so `j - i` decreases by exactly `1`.
- Initially `j - i = n - 1`, and termination occurs at `j - i = 0`.

Therefore the loop runs exactly `n - 1` iterations. The time complexity is `O(n)`, and the space complexity is `O(1)`.

## Appendix

### Worked Example
Consider `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`.

| Step | `i` | `j` | `H[i]` | `H[j]` | Width | Area | Best So Far | Move |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | 0 | 8 | 1 | 7 | 8 | `8 * min(1,7) = 8` | 8 | Move `i` because `H[0] < H[8]` |
| 2 | 1 | 8 | 8 | 7 | 7 | `7 * min(8,7) = 49` | 49 | Move `j` because `H[8] < H[1]` |
| 3 | 1 | 7 | 8 | 3 | 6 | `6 * min(8,3) = 18` | 49 | Move `j` because `H[7] < H[1]` |
| 4 | 1 | 6 | 8 | 8 | 5 | `5 * min(8,8) = 40` | 49 | Move either pointer |

The first row already exposes the pruning lemma: after evaluating `(0, 8)`, every pair `(0, k)` is narrower and still capped by height `1`.

### Visuals
Only the visuals that materially clarify the proof are kept here.

#### 1. Area Model
This is the geometric object being optimized: two boundaries determine both width and bottleneck height.

<div align="center">
  <img src="png/visual_1.png" alt="Problem layout with the optimal pair">
</div>

The area depends only on the chosen endpoints.

#### 2. Pruning a Boundary
This is the core proof move. After evaluating `(0, 8)`, the entire row anchored at `0` is dead because the left wall is already the bottleneck.

<div align="center">
  <img src="png/visual_4.png" alt="Pruning all pairs anchored at index zero">
</div>

The symmetric column argument is the reason the algorithm may always move the shorter side.

#### 3. Path Through the Search Space
The algorithm does not inspect the full upper-triangular state space. It walks one monotone path through it.

<div align="center">
  <img src="png/visual_8.png" alt="Single linear path through the quadratic state space">
</div>

That is why the algorithm examines only `n - 1` pairs instead of `n(n - 1)/2`.

#### 4. Invariant View
This picture captures the invariant: pruned cells are harmless, and any not-yet-dominated optimum must still lie inside the active window.

<div align="center">
  <img src="png/visual_9.png" alt="Invariant view of pruned cells and remaining search window">
</div>

The proof succeeds because pruning never deletes a pair that could improve on `best`.

### Why Naive / Wrong Approaches Fail
- **Brute force:** Evaluating every pair is correct but costs `n(n-1)/2 = O(n^2)` comparisons of candidate containers.
- **Move the taller pointer:** Width shrinks while the bottleneck height stays capped by the shorter wall, so the pruning lemma no longer applies.
- **Sort the heights first:** Sorting destroys the original index distances, so the width term in `A(i, j)` stops representing the actual problem.

### Common Pitfalls
- **Equal heights:** The proof is symmetric. On equality, either pointer can move safely.
- **Wrong loop guard:** `i <= j` introduces a width-`0` iteration that is not a valid container.
- **Two-element input:** When `n = 2`, there is exactly one valid pair, so the loop should execute once and stop.

### Variants / Follow-Ups
- **Return the maximizing indices.** Keep `best_i` and `best_j` whenever `best` improves. The proof is unchanged.
- **Use explicit x-coordinates instead of implicit indices.** Replace `j - i` with `x[j] - x[i]`. The pruning lemma still works because width strictly decreases when an endpoint moves inward.
