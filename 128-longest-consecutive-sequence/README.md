# 128: Longest Consecutive Sequence

- **Difficulty:** Medium
- **Tags:** Array, Hash Table
- **Pattern:** Hash-set chain starts

## Fundamentals

### Problem Contract
Given an unsorted integer array `nums`, return the length of the longest set of values that can be written as
```text
x, x+1, x+2, ..., x+k
```
with every value present in `nums`.

The positions in the original array do not matter; only value existence matters.

### Definitions and State Model
Let `S = set(nums)`. A value `x` is a chain start if `x-1` is not in `S`. For a chain start `x`, define its chain length as the number of consecutive values `x, x+1, ...` that belong to `S`.

### Key Lemma / Invariant / Recurrence
#### Chain-Start Lemma
Every consecutive sequence has exactly one chain start: its minimum value. Therefore it is sufficient to count forward only from values `x` such that `x-1` is absent.

#### Linear-Work Lemma
If counting begins only at chain starts, then each value in `S` is advanced through at most once across the entire algorithm. A value cannot belong to the forward scan of two different starts because consecutive sequences are disjoint by minimum value.

### Algorithm
1. Insert every value into `S`.
2. For each `x` in `S`, skip it if `x-1` is also in `S`.
3. Otherwise count `x, x+1, x+2, ...` until the chain ends.
4. Track the maximum chain length.

```text
S = set(nums)
best = 0
for x in S:
    if x - 1 in S:
        continue
    y = x
    while y in S:
        y += 1
    best = max(best, y - x)
return best
```

### Correctness Proof
By the chain-start lemma, every consecutive sequence has a unique minimum value `x` with `x-1` absent. When the algorithm visits that `x`, it counts exactly the members of that sequence until the first missing value, so it computes the exact length of that sequence.

Conversely, when the algorithm skips a value because `x-1` is present, that value is not the start of any maximal consecutive sequence, so skipping it loses no candidate length. Since every maximal consecutive sequence is counted at its unique start, and `best` stores the maximum among all counted lengths, the returned value is the longest consecutive length.

The linear-work lemma justifies the time bound but also clarifies that no sequence is partially recounted from multiple starts.

### Complexity Analysis
Let `n = len(nums)`.

- Building the hash set costs `O(n)` average time.
- The outer loop visits each distinct value once.
- By the linear-work lemma, the inner `while` loop advances through each distinct value at most once across all starts.

Therefore the average-case running time is `O(n)`, and the auxiliary space is `O(n)` for the set.

## Appendix

### Common Pitfalls
- Sorting first gives a correct `O(n log n)` solution, but it discards the main point of the hash-set proof.
- Iterating over the original array instead of the set complicates duplicate handling without improving the bound.
