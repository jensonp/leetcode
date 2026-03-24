# 97: Interleaving String

- **Difficulty:** Medium
- **Tags:** String, Dynamic Programming
- **Pattern:** 2D prefix-composition DP

## Fundamentals

### Problem Contract
Given strings `s1`, `s2`, and `s3`, return whether `s3` can be formed by interleaving `s1` and `s2` while preserving the internal order of characters from each source string.

A necessary condition is `len(s1) + len(s2) = len(s3)`.

### Definitions and State Model
Let `dp[i][j]` mean: the prefix `s3[0..i+j-1]` can be formed by interleaving `s1[0..i-1]` and `s2[0..j-1]`.

Base state:
```text
dp[0][0] = true.
```

### Key Lemma / Invariant / Recurrence
#### Prefix Recurrence
For `i, j >= 0` with `i + j > 0`:
```text
dp[i][j] =
    (i > 0 and dp[i-1][j] and s1[i-1] == s3[i+j-1])
 or (j > 0 and dp[i][j-1] and s2[j-1] == s3[i+j-1]).
```
The last character of the interleaving must come from the end of `s1` or the end of `s2`.

### Algorithm
Check the length condition, then fill the DP grid.

```text
if len(s1) + len(s2) != len(s3):
    return false
initialize dp of size (m+1) x (n+1)
dp[0][0] = true
for i in 0 .. m:
    for j in 0 .. n:
        if i > 0 and s1[i-1] == s3[i+j-1]:
            dp[i][j] |= dp[i-1][j]
        if j > 0 and s2[j-1] == s3[i+j-1]:
            dp[i][j] |= dp[i][j-1]
return dp[m][n]
```

### Correctness Proof
The length check is necessary because every character of `s3` must come from exactly one of `s1` or `s2`.

Assume the length check passes. The base state `dp[0][0] = true` is correct. For `i + j > 0`, any valid interleaving of the prefixes must end with either `s1[i-1]` or `s2[j-1]`, and that character must match `s3[i+j-1]`. Removing that last character leaves exactly one of the two smaller subproblems in the prefix recurrence. Conversely, if either smaller subproblem is true and the corresponding character matches, appending that character yields a valid interleaving. Therefore the recurrence is exact, and `dp[m][n]` is the desired answer.

### Complexity Analysis
Let `m = len(s1)` and `n = len(s2)`.

- The DP table has `(m+1)(n+1)` states.
- Each state is computed in `O(1)` time.

The running time is `O(mn)`. The auxiliary space is `O(mn)`, reducible to `O(n)` with a rolling row.

## Appendix

### Common Pitfalls
- Matching character counts alone is insufficient; interleaving also preserves the relative order inside `s1` and `s2`.
- A greedy choice of taking a matching character from one string first can fail when both sources share the same next character.
