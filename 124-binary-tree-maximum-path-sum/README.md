# 124: Binary Tree Maximum Path Sum

- **Difficulty:** Hard
- **Tags:** Tree, Depth-First Search, Dynamic Programming
- **Pattern:** Tree DP with downward gain and global optimum

## Fundamentals

### Problem Contract
A path is any nonempty sequence of nodes connected by parent-child edges, with no node repeated. The path may start and end anywhere in the tree. Return the maximum possible sum of node values over all such paths.

### Definitions and State Model
For each node `x`, define the downward gain
```text
gain(x) = maximum path sum of a path that starts at x and moves only downward through at most one child branch.
```
A path that uses `x` as its highest node may include:
- `x` alone,
- `x` plus a positive left gain,
- `x` plus a positive right gain,
- or `x` plus both positive gains, one on each side.

Maintain a global value `best` equal to the maximum path sum seen anywhere so far.

### Key Lemma / Invariant / Recurrence
#### Gain Recurrence
For node `x` with children `L` and `R`, let
```text
left = max(0, gain(L)),
right = max(0, gain(R)).
```
Then
```text
gain(x) = x.val + max(left, right).
```
Only one child branch may continue upward to the parent, so `gain(x)` keeps at most one side.

#### Through-Node Lemma
The maximum-sum path whose highest node is `x` has value
```text
x.val + left + right.
```
Therefore `best` must be updated with that quantity at every node.

### Algorithm
Run postorder DFS.

```text
best = -inf

dfs(node):
    if node is null:
        return 0
    left = max(0, dfs(node.left))
    right = max(0, dfs(node.right))
    best = max(best, node.val + left + right)
    return node.val + max(left, right)

dfs(root)
return best
```

### Correctness Proof
The DFS processes children before their parent, so when evaluating node `x`, the values `gain(L)` and `gain(R)` are already correct by induction.

The gain recurrence is correct because any downward path starting at `x` and continuing upward to `x`'s parent can use at most one child branch; using both would create a fork, which is not a path. Negative child gains are discarded because adding them would only decrease the sum.

The through-node lemma is correct because any path whose highest node is `x` can use at most one downward branch on the left and at most one on the right. Taking positive contributions from both sides gives the best path of that shape. Every simple path in the tree has a unique highest node, so updating `best` at every node considers every candidate path exactly at its highest node. Therefore the final `best` is the maximum path sum in the tree.

### Complexity Analysis
Let `n` be the number of nodes.

- Each node is visited once.
- Each visit does `O(1)` work beyond recursive calls.

The running time is `O(n)`. The auxiliary space is `O(h)` for recursion depth, where `h` is the tree height.

## Appendix

### Common Pitfalls
- Returning the through-node value `node.val + left + right` to the parent is incorrect because a parent path cannot continue through both child branches.
- Initializing `best` to `0` fails on trees whose node values are all negative.
