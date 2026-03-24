# 130: Surrounded Regions

- **Difficulty:** Medium
- **Tags:** Array, Depth-First Search, Breadth-First Search, Matrix
- **Pattern:** Boundary-reachable flood fill

## Fundamentals

### Problem Contract
Given an `m x n` board of `'X'` and `'O'`, capture every region of `'O'` that is fully surrounded by `'X'` by flipping those cells to `'X'`. Any `'O'` connected to the boundary through 4-directional `'O'` paths must remain `'O'`.

### Definitions and State Model
A cell is safe if it is an `'O'` connected to at least one boundary `'O'` by a 4-directional path of `'O'` cells.

The board can be partitioned into:
- safe `'O'` cells, which must survive,
- interior `'O'` cells not connected to the boundary, which must be captured.

### Key Lemma / Invariant / Recurrence
#### Boundary-Reachability Lemma
An `'O'` cell survives exactly when it is boundary-reachable. Any region not touching the boundary is surrounded and must be flipped.

### Algorithm
1. Start DFS or BFS from every boundary `'O'` and mark every reached `'O'` as safe, for example with a temporary symbol `'#'`.
2. Scan the board.
3. Flip remaining `'O'` cells to `'X'` and restore `'#'` back to `'O'`.

```text
for each boundary cell (r, c):
    if board[r][c] == 'O':
        mark_safe(r, c)
for each cell (r, c):
    if board[r][c] == 'O':
        board[r][c] = 'X'
    elif board[r][c] == '#':
        board[r][c] = 'O'
```

### Correctness Proof
By the boundary-reachability lemma, every cell reached from a boundary `'O'` must survive. Marking exactly those cells as safe preserves them through the final scan.

Any remaining `'O'` after the marking phase is not connected to the boundary, so it belongs to a surrounded region and must be flipped to `'X'`. Conversely, no marked safe cell is flipped to `'X'`; it is restored to `'O'` at the end. Therefore the final board captures exactly the surrounded regions.

### Complexity Analysis
Let the board size be `m x n`.

- Each cell is visited at most once by the boundary flood fill and once by the final scan.

The running time is `O(mn)`. The auxiliary space is `O(mn)` in the worst case for recursion or an explicit queue.

## Appendix

### Common Pitfalls
- Starting flood fill from interior `'O'` cells solves the wrong problem; the decisive property is boundary reachability.
- Flipping cells immediately during the boundary traversal can destroy the information needed to distinguish safe and captured regions.
