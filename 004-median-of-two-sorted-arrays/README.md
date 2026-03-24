# 4: Median of Two Sorted Arrays

- **Difficulty:** Hard
- **Tags:** Array, Binary Search, Divide and Conquer
- **Pattern:** Binary search on a partition boundary

## Fundamentals

### Problem Contract
Given two sorted arrays `A` and `B` of lengths `m` and `n`, return the median of the multiset `A ∪ B` in `O(log(m+n))` time.

If the total length `m+n` is odd, the median is the middle element. If it is even, the median is the average of the two middle elements.

### Definitions and State Model
Assume `m <= n`; otherwise swap the arrays. Choose a partition index `i` in `A` and define
```text
j = (m + n + 1) // 2 - i.
```
This makes the total number of elements on the left side equal to the total number on the right side, up to one extra element on the left when the total length is odd.

Define boundary values
```text
Aleft = A[i-1] if i > 0 else -inf
Aright = A[i] if i < m else +inf
Bleft = B[j-1] if j > 0 else -inf
Bright = B[j] if j < n else +inf
```

### Key Lemma / Invariant / Recurrence
#### Feasible-Partition Lemma
A partition `(i, j)` is correct exactly when
```text
Aleft <= Bright and Bleft <= Aright.
```
Then every value on the left side is at most every value on the right side, so the median is determined by the boundary values.

#### Binary-Search Direction Rule
- If `Aleft > Bright`, then `i` is too large and must move left.
- If `Bleft > Aright`, then `i` is too small and must move right.

These conditions are monotone because increasing `i` moves `Aleft` and `Aright` rightward in `A` while moving `Bleft` and `Bright` leftward in `B`.

### Algorithm
Binary search `i` on the smaller array.

```text
ensure len(A) <= len(B)
l = 0
r = m
while l <= r:
    i = (l + r) // 2
    j = (m + n + 1) // 2 - i
    compute Aleft, Aright, Bleft, Bright
    if Aleft <= Bright and Bleft <= Aright:
        if (m + n) is odd:
            return max(Aleft, Bleft)
        return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
    if Aleft > Bright:
        r = i - 1
    else:
        l = i + 1
```

### Correctness Proof
By construction, every candidate partition keeps the left side size fixed at `(m+n+1)//2`. The feasible-partition lemma says that such a partition is correct exactly when the two cross-boundary inequalities hold. In that case, the largest left value and smallest right value are the median boundaries: for odd total length the left side contains the extra element, so the median is `max(Aleft, Bleft)`; for even total length the median is the average of the two boundary values.

If `Aleft > Bright`, then the chosen partition takes too many elements from `A` into the left side, so every feasible partition must use a smaller `i`. If `Bleft > Aright`, then the partition takes too few elements from `A`, so every feasible partition must use a larger `i`. The binary-search direction rule therefore preserves the existence of a feasible partition inside the current search interval.

Because the search interval shrinks each step and a feasible partition exists, the algorithm eventually finds it and returns the correct median.

### Complexity Analysis
Assume `m <= n`.

- The binary search range on `i` has size `m + 1`.
- Each iteration performs `O(1)` work.

The running time is `O(log m) = O(log(min(m, n)))`, which is within `O(log(m+n))`. The auxiliary space is `O(1)`.

## Appendix

### Common Pitfalls
- Binary searching the larger array can make `j` leave the valid range; searching the smaller array avoids that issue cleanly.
- Using `(m+n)//2` instead of `(m+n+1)//2` breaks the odd-length case because the left side no longer contains the middle element.
