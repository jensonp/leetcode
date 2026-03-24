# 208: Implement Trie (Prefix Tree)

- **Difficulty:** Medium
- **Tags:** Hash Table, String, Design, Trie
- **Pattern:** Prefix tree with terminal markers

## Fundamentals

### Problem Contract
Implement a trie with operations:
- `insert(word)`,
- `search(word)`,
- `startsWith(prefix)`.

`search(word)` returns `true` only for a full inserted word. `startsWith(prefix)` returns `true` whenever some inserted word has that prefix.

### Definitions and State Model
Each trie node stores:
- a mapping `children` from characters to child nodes,
- a boolean `is_end` indicating whether the root-to-node path spells a complete inserted word.

The root represents the empty prefix.

### Key Lemma / Invariant / Recurrence
#### Prefix-Path Invariant
For every node `x`, the path label from the root to `x` is exactly one prefix of the inserted word set. Conversely, every inserted prefix has exactly one node reached by following its characters from the root.

#### Terminal-Marker Lemma
A word `w` has been inserted if and only if the node reached by following `w` exists and has `is_end = true`. Prefix existence alone is not enough.

### Algorithm
- `insert(word)`: create missing child edges while scanning the characters of `word`, then mark the terminal node.
- `search(word)`: follow the characters; succeed only if the final node exists and `is_end` is true.
- `startsWith(prefix)`: follow the characters; succeed if the final node exists.

```text
insert(word):
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = new TrieNode()
        node = node.children[ch]
    node.is_end = true

walk(s):
    node = root
    for ch in s:
        if ch not in node.children:
            return null
        node = node.children[ch]
    return node

search(word):
    node = walk(word)
    return node is not null and node.is_end

startsWith(prefix):
    return walk(prefix) is not null
```

### Correctness Proof
`insert` preserves the prefix-path invariant because it only creates nodes along the scanned characters of the inserted word. Existing nodes are reused, so equal prefixes share structure exactly as a trie should.

For `search(word)`, `walk(word)` succeeds exactly when the path for `word` exists. By the terminal-marker lemma, `search` returns `true` exactly for words whose terminal node is marked as a full word. For `startsWith(prefix)`, existence of the path is already the full condition, so returning whether `walk(prefix)` exists is correct.

Thus all operations satisfy their contracts.

### Complexity Analysis
Let `L` be the query string length.

- `insert`, `search`, and `startsWith` each scan at most `L` characters.
- Each child-map access is `O(1)` average time for a hash map or `O(Alphabet)` for a fixed array implementation.

Under average `O(1)` child access, each operation runs in `O(L)` time. The total space is `O(total inserted characters)` across all nodes.

## Appendix

### Common Pitfalls
- Marking every prefix node as terminal makes `search` behave like `startsWith`.
- Rebuilding strings at nodes is unnecessary; the structure already encodes the prefix.
