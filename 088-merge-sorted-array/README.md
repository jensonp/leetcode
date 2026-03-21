# 088: Merge Sorted Array

## Problem Restatement
We are given two integer arrays, `nums1` and `nums2`, both sorted in non-decreasing order. We are also given two integers `m` and `n`, representing the number of valid elements in `nums1` and `nums2` respectively.
Our goal is to merge `nums2` into `nums1` so that `nums1` becomes a single array sorted in non-decreasing order.

## Input/Output Interpretation
- **Input:** 
  - `nums1`: An array of size `m + n`. The first `m` elements are valid. The last `n` elements are `0`s, acting as placeholders for `nums2`.
  - `m`: Number of valid elements in `nums1`.
  - `nums2`: An array of size `n` containing elements to merge.
  - `n`: Number of elements in `nums2`.
- **Output:** None (in-place modification). `nums1` should be modified to contain the merged sorted elements.

## Constraints That Matter
- `nums1.length == m + n`
- `nums2.length == n`
- Both arrays are already sorted! This implies we shouldn't sort them again. We should use a merging technique (like in Merge Sort).
- In-place requirement: We cannot allocate a new array of size `m + n` to hold the merged result, so we must be clever about where we write values in `nums1` to avoid overwriting unread valid elements.

## Brute-Force Approach
A brute-force approach would be to copy all elements of `nums2` into the empty spaces at the end of `nums1` (indices `m` to `m + n - 1`), and then sort the entire `nums1` array using a built-in sort function.
- **Why it is weaker:** It completely ignores the fact that both arrays are *already* sorted. Sorting an array of size `m+n` takes $O((m+n) \log(m+n))$ time, which is suboptimal when we can linearly merge them in $O(m+n)$.

## Optimal Approach: Two Pointers from the Back
Since the end of `nums1` is empty (filled with `0`s), we can place the largest elements at the end without overwriting any valid elements we haven't processed yet.
We use three pointers:
- $p_1 = m - 1$ (points to the largest unmerged element in `nums1`)
- $p_2 = n - 1$ (points to the largest unmerged element in `nums2`)
- $p = m + n - 1$ (points to the last available position in `nums1`)

**Algorithm:**
1. Compare $nums1[p_1]$ and $nums2[p_2]$.
2. Place the larger value at $nums1[p]$.
3. Decrement $p$ and the pointer of the array we took the value from ($p_1$ or $p_2$).
4. Repeat this backward merge until all elements from `nums2` are successfully merged.

## Why the Optimal Approach Works
By starting from the *back*, we exploit the pre-allocated empty space in `nums1`. Since we always place the absolute largest remaining element at the very end of the array, and the number of empty spaces exactly equals the number of elements in `nums2`, we are mathematically guaranteed never to overwrite an element in `nums1` before it has a chance to be compared and safely moved!

## Visualizing the Algorithm

### Initial Array Setup
![Initial State](png/step0.png)

### Pointers Changing Over Time
When $nums2[p_2]$ is larger vs when $nums1[p_1]$ is larger or equal:

![After Step 1](png/step1.png)

![After Step 4](png/step4.png)

### Final State
The algorithm terminates here because `p2` has fallen below 0, indicating all elements from `nums2` have been successfully placed.

## Code Structure and Equations
```python
# p1 = m - 1
# p2 = n - 1
# p = m + n - 1
# 
# loop while p2 >= 0:
#   if p1 >= 0 and nums1[p1] > nums2[p2]:
#       nums1[p] = nums1[p1]
#       p1 -= 1
#   else:
#       nums1[p] = nums2[p2]
#       p2 -= 1
#   p -= 1
```

## Time and Space Complexity
- **Time Complexity:** $O(m + n)$. We process each element from `nums1` and `nums2` exactly once.
- **Space Complexity:** $O(1)$. We strictly merge in-place inside `nums1` without allocating additional array structures.

## Edge Cases
1. **`n == 0`**: `nums2` is empty. $p_2 = -1$ immediately. The loop doesn't run, and `nums1` is correctly untouched.
2. **`m == 0`**: `nums1` has no valid elements (is entirely `0`s). $p_1 = -1$ immediately. The loop will only execute the `else` block, safely copying all elements of `nums2` directly into `nums1`.
3. **Elements of `nums2` are entirely smaller than `nums1`**: `nums1` valid elements will all be shifted to the end first, and then `nums2` will seamlessly populate the front space.

## Common Pitfalls
- **Stopping condition logic check:** Using `while p1 >= 0 and p2 >= 0` and then forgetting to cleanly copy the remaining elements of `nums2` if `p1` exhausts first. If we just safely use `while p2 >= 0`, we handle the exhaustion of `nums1` inside the loop naturally with the `p1 >= 0` guard.
- **Overwriting data (Forward iteration):** Trying to merge from the front ($p_1 = 0, p_2 = 0$). This necessitates aggressively shifting elements or using a secondary array, which violates the $O(1)$ space requirement.

## Transferable Pattern Recognition
- **Two Pointers:** Whenever effectively merging sorted arrays or continuous lists, Two Pointers is the standard optimal baseline approach.
- **In-place Array Modification:** If an array has padding or empty space at the end, consider iterating and building the structured result **from back to front** avoiding overwriting important data.

## Self-Test Questions
1. Why does starting pointers from the *front* of `nums1` fail to be strictly $O(1)$ space?
2. What happens if $p_1 < 0$ but $p_2 \ge 0$? How does our code structural logic gracefully handle this?
3. What is the fundamental condition that strictly allows us to terminate the algorithm safely before $p_1$ reaches $0$?

## Next Step Before Coding
I must be completely able to trace the algorithm with pen and paper for the edge case where `m = 0` and `n = 3`. Once I can trace logically why $p_1 = -1$ allows `nums2` to naturally copy over via the `else` block, I am ready to implement this in my target language.
