# 088: Merge Sorted Array

# Problem Metadata
- LeetCode Number: 88
- Difficulty: Easy
- Topic Tags: Array, Two Pointers
- Primary Pattern: Two Pointers (Backwards)
- Secondary Pattern: In-Place Array Mutation
- Estimated Interview Signal: High (pointer logic, in-place safety, invariant reasoning)

# Problem Contract & Hidden Semantics

`nums1` has physical length `m + n`, but only its first `m` positions count as input data. The final `n` positions are spare capacity, not meaningful values. They happen to be `0`, but that is irrelevant — they are writable slots.

`nums2` has length `n`. All `n` elements are real input.

Both arrays are already sorted in non-decreasing order.

The function returns nothing (`void`). The answer must be written back into `nums1` itself. You cannot allocate and return a new array.

**Hidden assumptions:**
- "Sorted" means non-decreasing, so duplicates are allowed.
- The `0`s at the end of `nums1` are not part of the data. They are capacity.
- If `m = 0`, `nums1` still has total capacity `n`. There are no valid original elements, but there is room to copy all of `nums2` into it.
- If `n = 0`, `nums2` is empty. `nums1` is already the answer.

# Worked Example by Hand

**Input:** `nums1 = [1, 2, 3, 0, 0, 0]`, `m = 3`, `nums2 = [2, 5, 6]`, `n = 3`

We define pointers: `i = m-1 = 2`, `j = n-1 = 2`, `k = m+n-1 = 5`.

| Step | i | j | k | Compare | Action | nums1 state |
|------|---|---|---|---------|--------|-------------|
| 0 | 2 | 2 | 5 | `3` vs `6` | `6` wins, write to `[5]`, j-- | `[1, 2, 3, 0, 0, 6]` |
| 1 | 2 | 1 | 4 | `3` vs `5` | `5` wins, write to `[4]`, j-- | `[1, 2, 3, 0, 5, 6]` |
| 2 | 2 | 0 | 3 | `3` vs `2` | `3` wins, write to `[3]`, i-- | `[1, 2, 3, 3, 5, 6]` |
| 3 | 1 | 0 | 2 | `2` vs `2` | `2` (from B) wins via else, j-- | `[1, 2, 2, 3, 5, 6]` |
| 4 | 1 | -1 | 1 | j < 0 | Loop ends | `[1, 2, 2, 3, 5, 6]` |

After step 3, `j` drops below 0. The loop terminates. The remaining prefix `nums1[0..1] = [1, 2]` is already in correct sorted position because those elements were never moved and are smaller than everything placed after them.

# Clarifying Questions
- "Can elements be negative or contain duplicates?" — Yes. The logic is comparison-based and handles both.
- "If `m = 0`, does `nums1` still have length `n`?" — Yes. Capacity is always `m + n`.
- "Is extra space allowed?" — The problem expects $O(1)$ auxiliary space.

# Alternative Approaches & Tradeoffs

### 1. Append + Sort
- **Why it seems reasonable:** Copy `nums2` into the trailing slots of `nums1`, then sort. One line of code. Guaranteed correct.
- **The flaw:** It ignores that both inputs are already sorted. Sorting costs $O((m+n)\log(m+n))$ when a linear merge is possible.
- **Counterexample:** With `m = n = 500,000`, the sort does ~40× more comparisons than a merge.
- **Missing insight:** Because both arrays are sorted, we only ever need to compare the two current extremes — not re-sort globally.

### 2. Two Pointers from the Front
- **Why it seems reasonable:** This is how we merge two sorted linked lists. Compare heads, take the smaller, advance.
- **The flaw:** In an array, inserting at the front requires shifting everything to the right. Each insertion is $O(m)$, giving $O(m \cdot n)$ worst case. Alternatively, using a temporary array costs $O(m+n)$ space, violating the in-place constraint.
- **Counterexample:** If every element of `nums2` is smaller than `nums1[0]`, every insertion shifts the entire `m`-block.
- **Missing insight:** The spare capacity is at the **end** of `nums1`. Writing from the back avoids all shifting.

# Core Insight

The spare capacity sits at the tail of `nums1`. If we fill from the back — placing the largest remaining element at position `k` and working leftward — we write only into capacity slots. We never overwrite a valid element before reading it.

# Formal State Model

Let `A = nums1[0..m-1]` (original valid data), `B = nums2[0..n-1]`.

**State variables:**
- `i = m - 1` — index of the largest unplaced element in A
- `j = n - 1` — index of the largest unplaced element in B
- `k = m + n - 1` — index of the next write position in nums1

**Transition (each iteration):**
- If `i >= 0` and `A[i] > B[j]`: write `A[i]` to `nums1[k]`, decrement `i`
- Else: write `B[j]` to `nums1[k]`, decrement `j`
- Always decrement `k`

**Loop guard:** `j >= 0`

When `j < 0`, all of B has been placed. The remaining prefix of A is already in `nums1[0..i]` in sorted order, so no further work is needed.

# Correctness Proof

## Sorted-Suffix Invariant
**Claim:** After each iteration, `nums1[k+1 .. m+n-1]` contains the largest already-placed elements of `A ∪ B`, in sorted order.

- **Initialization:** Before the loop, no elements have been placed. The suffix `nums1[m+n .. m+n-1]` is empty, which is trivially sorted.
- **Maintenance:** Each iteration places the largest remaining candidate (either `A[i]` or `B[j]`) at position `k`. Since all previously placed values at `k+1..m+n-1` are ≥ this value (they were larger when chosen), appending to the left preserves sorted order.
- **Conclusion:** When the loop ends, the filled suffix is the complete sorted merge of all consumed elements.

## Safety Claim (No Overwrite)
Let `x` = number of elements taken from B so far, `y` = number taken from A. Then:

$$k = (m+n-1) - (x+y), \quad i = (m-1) - y$$

$$k - i = n - x$$

Since $x \le n$, we have $k - i \ge 0$. The write-head `k` never overtakes the read-head `i`. We never overwrite an unread element of A.

## Termination
Each iteration decrements `k` and either `i` or `j`. The loop runs at most `m + n` times. It exits when `j < 0`, meaning all of B has been placed. The remaining `A[0..i]` is already in its correct position in `nums1` (those elements were never moved and are ≤ everything in the filled suffix).

# Equation → Pseudocode → Code Mapping

**State variables → declarations:**
```
i = m - 1       # read-head for A
j = n - 1       # read-head for B
k = m + n - 1   # write-head
```

**Transition → loop body:**
```
while j >= 0:                         # loop guard: B not exhausted
    if i >= 0 and nums1[i] > nums2[j]:  # A's tail is larger
        nums1[k] = nums1[i]             # place A[i]
        i -= 1                           # advance A's read-head
    else:                                # B's tail is larger, or A exhausted
        nums1[k] = nums2[j]             # place B[j]
        j -= 1                           # advance B's read-head
    k -= 1                               # advance write-head
```

**Why `>` and not `>=` in the comparison:** Either works for correctness. Using `>` means ties go to B. Using `>=` means ties go to A. Both produce a valid sorted result. The choice does not affect complexity.

**Where bugs are most likely:**
- Using `while i >= 0 and j >= 0` instead of `while j >= 0`. The first form requires a second cleanup loop to copy remaining B elements. The single-guard form handles A-exhaustion inside the `if`.
- Off-by-one on initial pointer values. `i = m - 1`, not `m`. `k = m + n - 1`, not `m + n`.

# Visualizing the Algorithm

### 1. Problem Setup
Shows the physical layout: valid data vs. spare capacity in `nums1`.
![Problem Setup](png/setup.png)
The first 3 cells are real data. The last 3 are writable buffer — this is why backward merging works.

### 2. Why Append+Sort Wastes Work
Shows the brute-force approach discarding the sorted property entirely.
![Brute Force](png/bruteforce.png)
The red arrows dump `nums2` into the tail, then a full $O(N \log N)$ sort re-derives an ordering that already existed.

### 3. Backward Pointer Movement
Shows `i`, `j`, `k` resolving the largest elements into the buffer slots.
![Step 1](png/step1.png)
The write-head `k` moves left in lockstep with whichever read-head supplied the value.

### 4. Safety Invariant: k Never Overtakes i
Visually confirms the gap `k - i = n - x ≥ 0`.
![Invariant](png/invariant.png)
The gap can only shrink when we pull from B (increasing `x`), and `x` can never exceed `n`.

### 5. Edge Case: m = 0
When A is empty, `i = -1` immediately. The loop copies all of B into `nums1`.
![Edge Case](png/edge_case.png)
The `i >= 0` guard in the `if` prevents any read from the nonexistent A.

# Complexity Analysis
| Approach | Time | Space |
|----------|------|-------|
| Append + Sort | $O((m+n)\log(m+n))$ | $O(1)$ |
| Front merge + shift | $O(m \cdot n)$ | $O(1)$ |
| Front merge + temp array | $O(m+n)$ | $O(m+n)$ |
| **Backward merge** | **$O(m+n)$** | **$O(1)$** |

The backward merge is strictly dominant: linear time, constant space.

# Edge Cases & Pitfalls
- **`n = 0`:** Loop body never executes. `nums1` is untouched. Correct.
- **`m = 0`:** `i = -1`. Every iteration takes the `else` branch, copying B into `nums1`. Correct.
- **All of B smaller than all of A:** A elements fill the tail first, then B fills the front. The `j >= 0` guard handles the transition.
- **All duplicates:** Every comparison goes to `else` (B). Same logic, no special case needed.
- **Single-element arrays:** `m = 1, n = 1`. One comparison, one write, done.

# Transferable Pattern Recognition
- **Two Pointers on sorted data.** Trigger: two sorted sequences, merge/intersect/compare.
- **Back-to-front in-place fill.** Trigger: array has trailing capacity or padding. Writing from the back avoids shifting and overwrite hazards.

# Problem Variations & Follow-Ups
- **Merge Two Sorted Linked Lists (LC 21):** Same comparison logic, but front-to-back works because linked list insertion is $O(1)$. No shifting problem.
- **Merge K Sorted Lists (LC 23):** Two-pointer generalizes to a min-heap over K heads. Time becomes $O(N \log K)$.
- **Intersection of Two Sorted Arrays (LC 349/350):** Same two-pointer skeleton, but collect matches instead of merging all elements.

# Interview Questions

## In-Problem Follow-Ups
- "Why do you loop on `j >= 0` rather than `i >= 0 and j >= 0`?"
- "Can you prove the write-head never overwrites an unread element?"

## Post-Solution Probes
- "If `m` is huge and `n` is tiny (e.g., m=1M, n=5), is there a faster approach?" *(Yes — binary-search insertion of B's elements into A.)*
- "What changes if the problem asked you to return a new array instead of modifying in-place?"

# Self-Test Questions
1. State the safety invariant in one sentence. Why does `k - i = n - x` prove no overwrite?
2. Hand-trace the `m = 0, n = 3` case. What value does `i` start at, and why does the loop still work?
3. Why is `while j >= 0` sufficient as the sole loop guard?
4. If you used `>=` instead of `>` in the comparison, what changes? Does correctness break?
5. Why does the remaining prefix of A need no further work when `j` drops below 0?

# Next Step Before Coding
Hand-trace the `m = 0, n = 3` case on paper. Confirm that `i = -1` causes every iteration to take the `else` branch, copying B into `nums1[2], nums1[1], nums1[0]`. Once you can explain *why* this works without looking at notes, write the solution from memory.
