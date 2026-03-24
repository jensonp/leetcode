# 133: Clone Graph

- **Difficulty:** Medium
- **Tags:** Hash Table, Depth-First Search, Breadth-First Search, Graph
- **Pattern:** Graph copy with original-to-clone map

## Fundamentals

### Problem Contract
Given a reference to a node in a connected undirected graph, return a deep copy of the entire graph. Every original node must map to a unique clone, and every neighbor relation must be reproduced among clones.

### Definitions and State Model
Maintain a map `clone[x]` from each discovered original node `x` to its clone node `x'`.

The traversal may be DFS or BFS. The key state is that once `clone[x]` exists, every future edge incident to `x` can target the same clone node.

### Key Lemma / Invariant / Recurrence
#### Identity-Preservation Invariant
At all times, `clone` is a partial bijection between discovered original nodes and created clone nodes, and each created clone has the same value as its original.

#### Cycle-Safe Creation Rule
When first visiting node `x`, create `clone[x]` before traversing neighbors. Then any cycle that reaches `x` again can reuse the already created clone instead of recursing forever or creating duplicates.

### Algorithm
Run DFS from the input node.

```text
clone = empty map

dfs(x):
    if x in clone:
        return clone[x]
    x' = new Node(x.val)
    clone[x] = x'
    for y in x.neighbors:
        x'.neighbors.append(dfs(y))
    return x'

return dfs(node) if node else null
```

### Correctness Proof
When `dfs(x)` first creates `x'` and stores it in `clone`, the identity-preservation invariant begins to hold for `x`. For each neighbor `y`, the recursive call returns the unique clone `y'`, either by creating it or by reusing an existing one. Appending `y'` to `x'.neighbors` reproduces exactly the corresponding original edge.

The cycle-safe creation rule guarantees termination on cyclic graphs and prevents duplicate clones. Because the traversal starts from the given node and explores every reachable node, every original node and edge in the connected graph is copied exactly once into the clone graph. Therefore the returned node is the root of a correct deep copy.

### Complexity Analysis
Let `V` be the number of vertices and `E` the number of undirected edges.

- Each vertex is cloned once.
- Each adjacency list is scanned once.

The running time is `O(V + E)`. The auxiliary space is `O(V)` for the map and traversal stack or queue.

## Appendix

### Common Pitfalls
- Creating a new clone every time a node is revisited duplicates nodes and breaks graph identity.
- Deferring `clone[x] = x'` until after recursing on neighbors fails on cycles.
