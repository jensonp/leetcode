# 3: Longest Substring Without Repeating Characters

- **Difficulty:** Medium
- **Tags:** Hash Table, String, Sliding Window
- **Pattern:** Variable window with last-seen positions

## Fundamentals

### Problem Contract
Given a string `s`, return the maximum length of a contiguous substring whose characters are all distinct.

The output is a length, not the substring itself.

### Definitions and State Model
Maintain a window `[l, r]` and a table `last[c]` equal to the greatest index where character `c` has appeared so far.

For each step at index `r`, the intended invariant is that `s[l..r]` contains no repeated character. The best answer is
```text
best = max length of any valid window seen so far.
```

### Key Lemma / Invariant / Recurrence
#### Window Repair Lemma
When processing character `s[r]`, if its previous occurrence is at index `p = last[s[r]]`, then every valid window ending at `r` must start strictly after `p`. Therefore the left boundary may be updated by
```text
l = max(l, p + 1).
```
This discards exactly the prefixes that still contain a duplicate copy of `s[r]`.

#### Valid-Window Invariant
After updating `l` with the rule above, the window `s[l..r]` is duplicate-free and is the longest duplicate-free window ending at `r`.

### Algorithm
Scan `s` once from left to right.

```text
last = empty map
l = 0
best = 0
for r in 0 .. n-1:
    c = s[r]
    if c in last:
        l = max(l, last[c] + 1)
    last[c] = r
    best = max(best, r - l + 1)
return best
```

### Correctness Proof
Initially the window is empty, so the valid-window invariant holds vacuously.

Assume it holds before processing index `r`. Let `c = s[r]`. If `c` has not appeared in the current window, then keeping `l` unchanged preserves distinctness. If `c` previously appeared at `p >= l`, the window repair lemma shows that every duplicate-free window ending at `r` must start after `p`; updating `l` to `p+1` removes exactly the offending duplicate. Using `max` prevents `l` from moving backward when the previous occurrence lies outside the current window.

After the update, `s[l..r]` is duplicate-free and is the longest valid window ending at `r`, so updating `best` with its length is correct. Since every candidate answer is some valid window ending at some `r`, the maximum `best` seen over the scan is the maximum length over all duplicate-free substrings.

### Complexity Analysis
Let `n = len(s)`.

- Each index `r` is processed once.
- Each map lookup and update is `O(1)` on average.
- `l` only moves right.

Therefore the average-case running time is `O(n)` and the auxiliary space is `O(min(n, |Sigma|))`, where `|Sigma|` is the alphabet size.

## Appendix

### Common Pitfalls
- Updating `l` to `last[c] + 1` without `max` moves the window backward when the previous copy of `c` lies outside the current window.
- Treating this as a subsequence problem is incorrect; the substring must remain contiguous.
