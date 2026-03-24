# 51: N-Queens

- **Difficulty:** Hard
- **Tags:** Array, Backtracking
- **Pattern:** Row-by-row constraint search

## Fundamentals

### Problem Contract
Place `n` queens on an `n x n` board so that no two queens share a row, column, or diagonal. Return all valid boards.

### Definitions and State Model
Backtrack by row. At row `r`, maintain three forbidden sets:
- `cols` for occupied columns,
- `diag1` for occupied main diagonals identified by `r - c`,
- `diag2` for occupied anti-diagonals identified by `r + c`.

A state is `(r, cols, diag1, diag2, board_prefix)`.

### Key Lemma / Invariant / Recurrence
#### Row-Invariant
Before recursing on row `r`, the board prefix `0 .. r-1` contains exactly one queen per row and no attacking pair.

A column `c` is legal for row `r` exactly when `c not in cols`, `r-c not in diag1`, and `r+c not in diag2`.

### Algorithm
Try every legal column in the current row and recurse to the next row.

```text
ans = []

dfs(r):
    if r == n:
        record current board
        return
    for c in 0 .. n-1:
        if c in cols or r-c in diag1 or r+c in diag2:
            continue
        place queen at (r, c)
        add c, r-c, r+c to the forbidden sets
        dfs(r + 1)
        remove c, r-c, r+c from the forbidden sets
        remove queen at (r, c)
```

### Correctness Proof
The row-invariant holds initially for the empty prefix.

At row `r`, the legality test is exact: sharing a row is impossible by construction, and sharing a column or diagonal is equivalent to membership in the corresponding forbidden set. Therefore every recursive placement preserves the row-invariant.

If the recursion reaches `r = n`, then every row contains one queen and the invariant guarantees no attacks, so the recorded board is valid. Conversely, any valid solution determines one legal column choice per row. The DFS explores all legal choices, so it eventually visits the sequence corresponding to that solution and records it. Thus the algorithm enumerates exactly all valid boards.

### Complexity Analysis
The search tree is exponential. In the worst case, each row can branch to many columns, though pruning removes most branches in practice.

- The recursion depth is `n`.
- Each node performs `O(1)` legality checks with the sets.

The worst-case running time is exponential in `n`, and the auxiliary space is `O(n)` for the recursion stack and forbidden sets, excluding output storage.

## Appendix

### Common Pitfalls
- Scanning the whole board to test attacks at each step is correct but discards the point of the column/diagonal state model.
- Diagonal identities are `r-c` and `r+c`; using absolute differences merges distinct diagonals incorrectly.
