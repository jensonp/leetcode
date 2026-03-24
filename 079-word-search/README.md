# 79: Word Search

- **Difficulty:** Medium
- **Tags:** Array, String, Backtracking, Matrix
- **Pattern:** DFS with path-local visitation

## Fundamentals

### Problem Contract
Given a grid of characters and a word, return whether the word can be formed by a path of horizontally or vertically adjacent cells, using each cell at most once in that path.

### Definitions and State Model
A DFS state is `(r, c, k)` meaning: can a path starting at cell `(r, c)` match the suffix `word[k..]` while respecting the path-local used-cell constraint?

### Key Lemma / Invariant / Recurrence
#### DFS State Recurrence
State `(r, c, k)` is feasible exactly when:
- `(r, c)` is inside the grid,
- `board[r][c] == word[k]`,
- and if `k` is not the last index, at least one 4-neighbor matches state `(next_r, next_c, k+1)` after marking `(r, c)` as used for the current path.

The used-cell constraint is path-local, so a cell may be reused by different starting points, but not twice in one recursive branch.

### Algorithm
Try DFS from every grid cell.

```text
for each cell (r, c):
    if dfs(r, c, 0):
        return true
return false

dfs(r, c, k):
    if board[r][c] != word[k]:
        return false
    if k == len(word) - 1:
        return true
    temporarily mark (r, c) as used
    for each 4-neighbor (nr, nc):
        if inside grid and not used and dfs(nr, nc, k + 1):
            return true
    unmark (r, c)
    return false
```

### Correctness Proof
The DFS state recurrence is an exact reformulation of the problem contract: the next character must match the current cell, and the rest of the word must be realized by one adjacent continuation without reusing the same cell in that path.

If the algorithm returns `true`, it found a recursive branch satisfying the recurrence at every step, so the corresponding grid path spells the word. Conversely, any valid path for the word defines a sequence of DFS choices that the algorithm explores from its starting cell. Therefore if a valid path exists, some DFS call returns `true`.

### Complexity Analysis
Let the board size be `m x n` and `L = len(word)`.

- There are `mn` starting cells.
- From each step after the first, the DFS has at most `3` forward choices because it cannot immediately revisit the previous cell.

A standard worst-case bound is `O(mn * 3^(L-1))` time, with `O(L)` auxiliary space for the recursion path.

## Appendix

### Common Pitfalls
- Using a global visited set across different starting cells is incorrect; visitation is local to one candidate path.
- Forgetting to unmark a cell on backtracking blocks valid paths in sibling branches.
