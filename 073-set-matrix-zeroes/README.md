# 73: Set Matrix Zeroes

- **Difficulty:** Medium
- **Tags:** Array, Matrix
- **Pattern:** In-place metadata encoding

## Fundamentals

### Problem Contract
Given an `m x n` matrix, if any entry is `0`, set its entire row and entire column to `0` in place.

The update is based on the original zero positions, not on zeros written later during the process.

### Definitions and State Model
Use the first row and first column as marker storage:
- `matrix[i][0] = 0` marks that row `i` must be zeroed,
- `matrix[0][j] = 0` marks that column `j` must be zeroed.

Because `matrix[0][0]` cannot independently represent both the first row and the first column, keep two booleans:
- `first_row_zero`,
- `first_col_zero`.

### Key Lemma / Invariant / Recurrence
#### Marker Sufficiency Lemma
After scanning the matrix once and writing markers into the first row and first column, the pair `(first_row_zero, first_col_zero)` together with the marker cells determines exactly which rows and columns must be zeroed.

The key point is temporal separation: the first pass reads the original matrix and writes only metadata. The second pass interprets that metadata without confusing newly written zeros with original zeros.

### Algorithm
1. Scan the first row and first column to set `first_row_zero` and `first_col_zero`.
2. Scan the interior cells. For every original zero at `(i, j)` with `i > 0`, `j > 0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`.
3. Scan the interior again. Zero `(i, j)` whenever its row marker or column marker is zero.
4. Zero the first row if `first_row_zero`.
5. Zero the first column if `first_col_zero`.

```text
first_row_zero = any(matrix[0][j] == 0)
first_col_zero = any(matrix[i][0] == 0)
for i in 1 .. m-1:
    for j in 1 .. n-1:
        if matrix[i][j] == 0:
            matrix[i][0] = 0
            matrix[0][j] = 0
for i in 1 .. m-1:
    for j in 1 .. n-1:
        if matrix[i][0] == 0 or matrix[0][j] == 0:
            matrix[i][j] = 0
if first_row_zero: zero row 0
if first_col_zero: zero column 0
```

### Correctness Proof
The first pass records exactly the rows and columns that contain an original zero. The marker sufficiency lemma shows that no required row or column is omitted, and none is falsely added except through an original zero witness.

During the second interior pass, an interior cell `(i, j)` is set to zero exactly when row `i` or column `j` was marked. That matches the contract because those markers were created precisely from original zeros. The first row and first column are handled separately using the saved booleans, so the ambiguity at `matrix[0][0]` does not corrupt the result.

Therefore every cell that must become zero does become zero, and every cell that should remain unchanged is preserved until one of its original row or column constraints requires zeroing.

### Complexity Analysis
Let the matrix size be `m x n`.

- Each pass touches `O(mn)` cells.
- The algorithm stores only two booleans beyond the reused marker cells.

The running time is `O(mn)` and the auxiliary space is `O(1)`.

## Appendix

### Common Pitfalls
- Zeroing rows and columns immediately during the first scan contaminates later decisions with zeros that were not present in the original matrix.
- Using only `matrix[0][0]` without separate booleans loses the ability to distinguish the first row from the first column.
