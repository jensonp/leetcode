# 138: Copy List with Random Pointer

- **Difficulty:** Medium
- **Tags:** Hash Table, Linked List
- **Pattern:** Structural copying with interleaved clones

## Fundamentals

### Problem Contract
Each node has fields `val`, `next`, and `random`. Return a deep copy of the list: every original node must map to a distinct clone with the same `val`, and clone pointers must reproduce the `next` and `random` structure using only clone nodes.

### Definitions and State Model
Use the interleaving construction. For each original node `x`, insert its clone `x'` immediately after it:
```text
x -> x' -> old_next.
```
After this first pass, `x.next` is the clone of `x`.

### Key Lemma / Invariant / Recurrence
#### Clone-Access Lemma
After interleaving, if original node `x.random = y`, then the correct clone target for `x'` is `y' = y.next`. Thus
```text
x'.random = x.random.next
```
whenever `x.random` is not null.

#### Separation Invariant
After the third pass, the original list is restored exactly, and the extracted clone list preserves every `next` and `random` edge among clones.

### Algorithm
1. First pass: create `x'` after every original `x`.
2. Second pass: set `x'.random = x.random.next` when `x.random` exists.
3. Third pass: detach the interleaved structure into the original list and the clone list.

```text
cur = head
while cur:
    clone = Node(cur.val)
    clone.next = cur.next
    cur.next = clone
    cur = clone.next

cur = head
while cur:
    if cur.random:
        cur.next.random = cur.random.next
    cur = cur.next.next

cur = head
clone_head = head.next if head else null
while cur:
    clone = cur.next
    cur.next = clone.next
    clone.next = clone.next.next if clone.next else null
    cur = cur.next
return clone_head
```

### Correctness Proof
After the first pass, every original node `x` has exactly one adjacent clone `x'`, so the mapping from originals to clones is explicit in the list itself. The clone-access lemma then proves the second pass correct: because `y'` sits immediately after `y`, assigning `x'.random = x.random.next` recreates the original random edge on clones.

During the third pass, each original `x` skips over `x'` to its original successor, restoring the original `next` chain. Simultaneously each clone `x'` skips over the next original node to the next clone, forming the clone `next` chain. No `random` edge is changed in this pass, so the structure established in pass two remains intact. Therefore the extracted clone list is a deep copy and the original list is restored.

### Complexity Analysis
Let `n` be the number of nodes.

- Each of the three passes touches each node `O(1)` times.

The running time is `O(n)`. The auxiliary space is `O(1)` beyond the newly allocated clone nodes.

## Appendix

### Common Pitfalls
- Copying only values and `next` links without preserving node identity for `random` pointers is not a deep copy.
- Detaching the interleaved list before assigning `random` pointers loses the constant-time access from `x` to `x'`.
