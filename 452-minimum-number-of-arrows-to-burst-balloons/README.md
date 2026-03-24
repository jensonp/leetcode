# 452: Minimum Number of Arrows to Burst Balloons

- **Difficulty:** Medium
- **Tags:** Array, Greedy, Sorting
- **Pattern:** Earliest-finish greedy stabbing

## Fundamentals

### Problem Contract
Each balloon is a closed interval `[start, end]` on the x-axis. One arrow shot at position `x` bursts every balloon with `start <= x <= end`. Return the minimum number of arrows needed to burst all balloons.

### Definitions and State Model
Sort balloons by increasing end coordinate. Maintain:
- `arrow_pos` = position of the most recently chosen arrow,
- `count` = number of arrows used.

### Key Lemma / Invariant / Recurrence
#### Earliest-End Greedy Lemma
Among all remaining balloons, choose the one with smallest end `e` and shoot an arrow at `e`. This arrow bursts that balloon and every other remaining balloon whose interval contains `e`. No optimal solution can do better on the first arrow, because every solution must place its first arrow inside the earliest-ending balloon, and placing it at `e` only weakly increases the set of later balloons it can still hit.

### Algorithm
1. Sort by end.
2. Shoot the first arrow at the first end.
3. For each later interval, if its start is greater than `arrow_pos`, it is not burst yet, so shoot a new arrow at its end.

```text
sort balloons by end
count = 0
arrow_pos = -inf
for [start, end] in balloons:
    if start > arrow_pos:
        count += 1
        arrow_pos = end
return count
```

### Correctness Proof
By the earliest-end greedy lemma, there exists an optimal solution whose first arrow is shot at the end of the earliest-ending balloon. After shooting there, every burst balloon can be removed, and the remaining problem has the same form on the remaining intervals.

The algorithm repeats exactly this choice after each removal. Therefore, by induction on the number of remaining balloons, each chosen arrow can be part of some optimal solution for the corresponding subproblem. Hence the total number of arrows used by the algorithm is optimal.

### Complexity Analysis
Let `n` be the number of balloons.

- Sorting costs `O(n log n)`.
- The scan after sorting is `O(n)`.

The running time is `O(n log n)`. The auxiliary space is `O(1)` beyond sort workspace if sorting in place, or `O(n)` depending on the sort implementation.

## Appendix

### Common Pitfalls
- Sorting by start instead of end breaks the greedy proof.
- Using `start >= arrow_pos` instead of `start > arrow_pos` incorrectly adds an extra arrow when a balloon begins exactly where the previous arrow was shot.
