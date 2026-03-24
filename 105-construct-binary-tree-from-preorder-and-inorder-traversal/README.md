# 105: Construct Binary Tree from Preorder and Inorder Traversal

- **Difficulty:** Medium
- **Tags:** Array, Hash Table, Divide and Conquer, Tree
- **Pattern:** Recursive subtree sizing from traversals

## Fundamentals

### Problem Contract
Given the preorder and inorder traversals of a binary tree with distinct values, reconstruct the unique tree and return its root.

Distinctness matters because repeated values would make the inorder split ambiguous.

### Definitions and State Model
Preorder visits nodes as `root, left subtree, right subtree`. Inorder visits them as `left subtree, root, right subtree`.

Maintain:
- an index map `pos[value]` giving the inorder position of each value,
- a pointer `pre_idx` to the next root value in preorder,
- recursive bounds `[L, R]` inside the inorder array for the current subtree.

### Key Lemma / Invariant / Recurrence
#### Traversal-Split Lemma
For a subtree whose inorder segment is `[L, R]`, the next preorder value is its root `root_val`. Let `m = pos[root_val]`. Then:
- inorder `[L, m-1]` is the left subtree,
- inorder `[m+1, R]` is the right subtree,
- the left subtree must be constructed before the right subtree so that preorder consumption stays aligned.

### Algorithm
Recurse on inorder segments.

```text
pre_idx = 0
pos = map from inorder value to index

build(L, R):
    if L > R:
        return null
    root_val = preorder[pre_idx]
    pre_idx += 1
    m = pos[root_val]
    root = Node(root_val)
    root.left = build(L, m - 1)
    root.right = build(m + 1, R)
    return root

return build(0, n - 1)
```

### Correctness Proof
For an empty inorder segment, returning `null` is correct.

Now consider a nonempty segment `[L, R]`. By preorder semantics, the next unread preorder value is the root of this subtree. By inorder semantics, that root splits the segment into exactly the left subtree values and right subtree values. The traversal-split lemma therefore identifies the two recursive subproblems uniquely.

Because preorder lists all left-subtree nodes before all right-subtree nodes, constructing the left subtree first consumes exactly the correct number of preorder values before the right subtree begins. By induction on subtree size, both recursive calls construct the correct subtrees. Therefore the assembled root is the unique tree matching both traversals.

### Complexity Analysis
Let `n` be the number of nodes.

- Building the index map costs `O(n)`.
- Each node is created once and looked up once in the map.

The running time is `O(n)`. The auxiliary space is `O(n)` for the map and recursion stack in the worst case.

## Appendix

### Common Pitfalls
- Searching linearly for the root position inside inorder at every call degrades the running time to `O(n^2)`.
- Reconstructing the right subtree before the left subtree consumes preorder in the wrong order.
