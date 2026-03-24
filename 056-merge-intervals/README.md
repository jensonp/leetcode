# 56: Merge Intervals

- **Difficulty:** Medium
- **Tags:** Array, Sorting
- **Pattern:** Sort and sweep with merged-prefix invariant

## Fundamentals

### Problem Contract
Given intervals `[start, end]`, return a list of disjoint intervals whose union is the same as the union of the input intervals.

Two intervals overlap exactly when the later start is at most the earlier end.

### Definitions and State Model
Sort the intervals by increasing start. Maintain a result list `merged`.

At any moment, `merged[-1]` is the merged interval for the rightmost connected component among the processed intervals.

### Key Lemma / Invariant / Recurrence
#### Merged-Prefix Invariant
After processing the first `k` sorted intervals, `merged` is a sorted list of disjoint intervals whose union equals the union of those `k` intervals.

#### Local Merge Lemma
Let `I` be the next interval in start-sorted order.
- If `I.start > merged[-1].end`, then `I` begins a new connected component and must be appended.
- Otherwise `I` overlaps the rightmost component, and replacing `merged[-1].end` by `max(merged[-1].end, I.end)` preserves the same union.

### Algorithm
1. Sort by start.
2. Initialize `merged` with the first interval.
3. Sweep through the remaining intervals.
4. Apply the local merge lemma against `merged[-1]`.

```text
sort intervals by start
merged = []
for interval in intervals:
    if merged is empty or interval.start > merged[-1].end:
        append interval to merged
    else:
        merged[-1].end = max(merged[-1].end, interval.end)
return merged
```

### Correctness Proof
After sorting, any future overlap with the current interval can only occur with the rightmost merged interval, because all earlier merged intervals end no later than `merged[-1]` and are already disjoint from it.

Assume the merged-prefix invariant holds before processing `I`. If `I.start > merged[-1].end`, then `I` is disjoint from the rightmost component and, by sorted order, from every earlier component as well. Appending `I` preserves sorted disjointness and adds exactly its union. If `I.start <= merged[-1].end`, then `I` lies in the same connected component as `merged[-1]`; extending the end to `max(...)` preserves the exact union of that component. Thus the invariant is maintained.

When the sweep ends, the invariant says `merged` is disjoint, sorted, and has the same union as all input intervals. That is exactly the required output.

### Complexity Analysis
Let `n` be the number of intervals.

- Sorting costs `O(n log n)`.
- The sweep performs `O(n)` comparisons and updates.

The total time is `O(n log n)`. The auxiliary space is `O(n)` for the output, plus any sort workspace required by the implementation.

## Appendix

### Common Pitfalls
- Merging based on strict inequality `I.start < merged[-1].end` incorrectly leaves touching intervals such as `[1,4]` and `[4,5]` separated.
- Sorting by end instead of start destroys the local-merge proof.
