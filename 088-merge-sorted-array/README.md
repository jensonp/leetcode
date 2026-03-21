# 088: Merge Sorted Array

## Problem Restatement & Implications
We are given two integer arrays, `nums1` and `nums2`, both sorted in non-decreasing order. We also have integers `m` and `n`, representing the valid elements in `nums1` and `nums2` respectively.
Our goal is to merge `nums2` into `nums1` so that `nums1` becomes a single array sorted in non-decreasing order.

**Implications of Inputs/Outputs and Constraints:** 
  - `nums1` has a total pre-allocated length of `m + n`. The first `m` elements are valid data, while the last `n` elements are `0`s acting as raw buffer space.
  - Return type is `void`; we must modify `nums1` strictly **in-place**.
  - Arrays are already sorted. This is a massive hint that $O((m+n)\log(m+n))$ sorting is suboptimal, and we should capitalize on the existing order to achieve $O(m+n)$ linear merging.

---

## Alternative Approaches & Tradeoffs

### 1. Concat and Built-in Sort (Brute Force)
- **The Idea:** Concatenate the active `n` elements of `nums2` into the trailing `0`s of `nums1`, then call a built-in library sort.
- **Why it seems attractive:** Extremely fast to write, usually one line in modern languages, low cognitive load.
- **Why it falls short:** Time complexity is $O((m+n)\log(m+n))$. It entirely ignores the fact that both arrays are already sorted. In an interview, treating sorted input as unsorted demonstrates a lack of analytical observation.
- **The Missing Insight:** We don't need to perform general comparisons globally; local comparisons between the heads (or tails) of the arrays are sufficient.

### 2. Two Pointers from the Front with Shifting
- **The Idea:** Place pointers at index 0 of both arrays. If $nums2[p_2] < nums1[p_1]$, insert the element into $nums1$ and shift every remaining element in $nums1$ to the right to make space.
- **Why it seems attractive:** Reading left-to-right is natural to human intuition. It mimics how we merge Linked Lists.
- **Why it falls short:** Arrays are contiguous memory blocks. Shifting elements to the right takes $O(m)$ time per insertion. In the worst case, this inflates the time complexity to $O((m+n)^2)$. Attempting to avoid shifting by creating a temporary output array requires $O(m+n)$ auxiliary space, failing the in-place constraint.
- **The Missing Insight:** The empty buffer space in `nums1` is located at the **end**, not the beginning. We should iterate towards the buffer to avoid colliding with unread data.

---

## Optimal Approach: Two Pointers from the Back
Since the empty space is trailing, we can sort the arrays in reverse (largest to smallest) and place the largest elements at the very back of `nums1`.

**Algorithm Step-by-Step:**
1. Initialize three pointers: $p_1$ pointing to the end of `nums1`'s valid data ($m-1$), $p_2$ pointing to the end of `nums2` ($n-1$), and $p$ pointing to the literal end of `nums1` ($m+n-1$).
2. While elements remain in `nums2` ($p_2 \ge 0$):
3. Compare the elements at $nums1[p_1]$ and $nums2[p_2]$.
4. Take the larger of the two, place it at $nums1[p]$, and decrement the $p$ pointer and the pointer from which the element was taken.
5. If $p_1$ exhausts early, naturally copy the rest of `nums2` over.

### Mathematical Reasoning & Invariants
**Invariant:** At any step $k$, the number of filled elements at the tail of `nums1` is exactly the number of elements processed from `nums1` + `nums2`.
Because $p = (m-1) + (n-1) - k$, and we only ever write to $p$, the available space ($nums1$ buffer) perfectly mathematically guarantees we will **never** overwrite an element in `nums1` before $p_1$ has had a chance to read it!

---

## Visualizing the Algorithm

### 1. Problem Setup 
Shows the pre-allocated buffer trailing at the end, leading to the insight of backward merging.
![Initial State](png/step0.png)

### 2. Backward Pointer Movement Transition
Shows the pointers safely resolving the largest elements into the buffer.
![After Step 1](png/step1.png)

### 3. Edge-Case Graceful Handling
By the late stages, elements are safely sliding into their relative local spaces without collision.
![After Step 4](png/step4.png)

---

## Code Structure (Pseudocode Logic)
```python
# Initialize pointers at the tails
p1 = m - 1
p2 = n - 1
p = m + n - 1

# Only nums2 dictates the critical loop termination
while p2 >= 0:
    if p1 >= 0 and nums1[p1] > nums2[p2]:
        # nums1 element is larger
        nums1[p] = nums1[p1]
        p1 -= 1
    else:
        # nums2 element is larger (or p1 exhausted)
        nums1[p] = nums2[p2]
        p2 -= 1
    p -= 1
```

---

## Complexity Analysis
- **Time Complexity:** $O(m + n)$. We touch each element in both arrays exactly once, doing $O(1)$ operations per element.
- **Space Complexity:** $O(1)$. We strictly mutate `nums1` in place without allocating auxiliary arrays (pointers require negligible, constant space).

## Edge Cases & Pitfalls
- **Edge Case 1: `n == 0`**: Loop never runs. `nums1` is perfectly untouched. Safe.
- **Edge Case 2: `m == 0`**: $p_1 = -1$ immediately. The conditional falls straight to the `else` block, smoothly copying all of `nums2` into `nums1`. Safe.
- **Pitfall:** `while p1 >= 0 and p2 >= 0:` loop logic. Using this structure requires a second manually unrolled `while p2 >= 0` loop afterward to catch elements if $nums1$ ran out first. The structure provided above uses a cleaner single loop because it delegates the exhaustion of $p_1$ to the `if` condition itself.

## Transferable Pattern Recognition
- **Two Pointers:** Canonical approach for merging, comparing, or reconciling pairs of sorted sequences.
- **In-place Array Modification (Back-to-Front Traversal):** When an array has padding to absorb new data, starting from the back prevents rippling shift operations and data overwrites.

---

## Problem Variations & Follow-Ups
- **Variation: Merge Sorted Linked Lists (LeetCode 21)**
  - *Twist:* Arrays are swapped for Linked Lists.
  - *Approach:* We merge **front-to-back**. Because Linked List pointer manipulation takes $O(1)$ time and doesn't require shifting neighbor nodes in memory, front-to-back is optimal.
- **Variation: Merge 'K' Sorted Arrays (LeetCode 23)**
  - *Twist:* Generalizing 2 arrays to $K$ arrays.
  - *Approach:* Two-pointers upgrade into a **Min-Heap (Priority Queue)** to efficiently track the smallest/largest element across $K$ heads simultaneously.

---

## Interview Simulation Questions

### Clarifying Questions (Ask Before Coding)
- "Are there negative numbers? Elements with duplicate values?" *(Yes, the logic handles duplicates via `>=`).*
- "If $m=0$, does `nums1` still have a length of $n$?" *(Yes, it's strictly pre-allocated).*

### In-Problem Follow-Ups (During the Solve)
- "Why does your main loop only check `p2 >= 0` instead of `p1 >= 0 and p2 >= 0`?"
- "Can you guarantee that $p$ will never overwrite $p_1$?" 

### Post-Solution Probes
- "If this was running in a highly constrained embedded system with almost zero L1 Cache, would you still use this array traversal?"
- "What if `nums1` was much, much larger than `nums2` (e.g., $m = 1,000,000$, $n=10$)? Does the Time Complexity change your algorithm choice?" *(Hint: Binary Search merging).*

### Role-Relevant Technical Questions
- "If you were merging millions of arrays originating from independent microservice packet streams, how would you design the aggregation system rather than just a single loop?"

---

## Self-Test Questions
1. How does navigating `nums1` back-to-front solve the $O(1)$ space constraint?
2. Trace the single-loop `if/else` logic exactly when `p1` hits `-1`. How does the code proceed without an `IndexOutOfBounds` error?
3. What is the Big-O Time Complexity of inserting into an array's first index (`0`) and why does that invalidate left-to-right processing here?

## Next Step Before Coding
Ensure you can draw the array pointers on paper and articulate *why* $p$ never collides with $p_1$ before $p_1$ moves, fundamentally proving the non-overwrite invariant. Once verbally defended, implement the algorithm.
