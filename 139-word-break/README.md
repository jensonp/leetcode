# 139: Word Break

- **Difficulty:** Medium
- **Tags:** Hash Table, String, Dynamic Programming
- **Pattern:** Prefix segmentation DP

## Fundamentals

### Problem Contract
Given a string `s` and a dictionary `wordDict`, return whether `s` can be segmented into a sequence of dictionary words.

### Definitions and State Model
Let `dp[i]` mean: the prefix `s[0..i-1]` is segmentable.

Base state:
```text
dp[0] = true.
```
This encodes the empty prefix.

### Key Lemma / Invariant / Recurrence
#### Segmentation Recurrence
For `i > 0`,
```text
dp[i] = true iff there exists j < i with dp[j] = true and s[j:i] in dict.
```
The final dictionary word in any valid segmentation must begin at some `j`, leaving a segmentable prefix before it.

### Algorithm
Fill `dp` left to right.

```text
dict = set(wordDict)
dp = [false] * (n + 1)
dp[0] = true
for i in 1 .. n:
    for j in 0 .. i-1:
        if dp[j] and s[j:i] in dict:
            dp[i] = true
            break
return dp[n]
```

### Correctness Proof
The base case `dp[0] = true` is correct because the empty string needs no words.

Assume all earlier `dp` values are correct. If `dp[i]` becomes true, then the recurrence provides an index `j` such that `dp[j]` is true and `s[j:i]` is in the dictionary. By induction, `s[0:j]` has a valid segmentation, so appending `s[j:i]` gives a valid segmentation of `s[0:i]`.

Conversely, if `s[0:i]` has a valid segmentation, let the last dictionary word begin at `j`. Then `s[0:j]` is segmentable, so `dp[j]` is true by induction, and the recurrence will set `dp[i]` to true. Therefore `dp[i]` is true exactly for segmentable prefixes, and the answer is `dp[n]`.

### Complexity Analysis
Let `n = len(s)`.

- There are `O(n^2)` pairs `(j, i)`.
- Each pair does a dictionary lookup on `s[j:i]`.

In a model where substring extraction is `O(1)`, the running time is `O(n^2)`. In languages where slicing copies characters, the practical bound can be `O(n^3)` unless substring views or rolling hashes are used. The auxiliary space is `O(n + |dict|)`.

## Appendix

### Common Pitfalls
- Greedily taking the longest available dictionary word can block a valid segmentation later.
- Using only a set of prefix lengths is insufficient; the recurrence depends on which specific substrings are dictionary words.
