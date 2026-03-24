# 25: Reverse Nodes in k-Group

- **Difficulty:** Hard
- **Tags:** Linked List
- **Pattern:** Segment rewiring with boundary pointers

## Fundamentals

### Problem Contract
Given a linked list and an integer `k`, reverse the nodes of the list in contiguous groups of size `k`. If fewer than `k` nodes remain at the end, leave that suffix unchanged.

Only pointers may be rewired; node values may not be copied between nodes.

### Definitions and State Model
Maintain a dummy node before the head and a pointer `group_prev` whose `next` field is the first node of the next group candidate.

For each iteration:
- `kth` is the `k`th node after `group_prev`, if it exists,
- `group_next = kth.next` is the node after the group.

The segment to reverse is exactly the half-open chain `[group_prev.next, group_next)`.

### Key Lemma / Invariant / Recurrence
#### Group-Existence Lemma
If fewer than `k` nodes remain after `group_prev`, then no further reversal is allowed by the contract, so the algorithm must stop.

#### Processed-Prefix Invariant
Before each iteration, the list prefix ending at `group_prev` is already in final form, and the remainder starting at `group_prev.next` is exactly the untouched suffix of the original list.

### Algorithm
1. Use `group_prev` to locate `kth`.
2. If `kth` does not exist, stop.
3. Reverse the pointers on `[group_prev.next, group_next)`.
4. Splice the reversed group back after `group_prev`.
5. Advance `group_prev` to the tail of the reversed group and repeat.

```text
dummy.next = head
group_prev = dummy
while true:
    kth = advance k steps from group_prev
    if kth is null:
        break
    group_next = kth.next
    prev = group_next
    cur = group_prev.next
    while cur != group_next:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    new_tail = group_prev.next
    group_prev.next = kth
    group_prev = new_tail
return dummy.next
```

### Correctness Proof
Initially the processed prefix is empty, so the invariant holds.

Assume it holds before an iteration. If `kth` does not exist, the group-existence lemma applies, so the remaining suffix has length less than `k` and must remain unchanged. Stopping is correct.

Otherwise the inner reversal loop reverses exactly the edges inside `[group_prev.next, group_next)` and points the new tail to `group_next`. This produces the correct reversed group without affecting nodes outside the segment. Splicing `kth` after `group_prev` attaches that reversed segment to the already finalized prefix. The old group head becomes the new tail, so moving `group_prev` to that node restores the processed-prefix invariant for the next iteration.

By induction, every complete block of size `k` is reversed and the final short suffix, if any, is preserved. Therefore the returned list satisfies the contract.

### Complexity Analysis
Let `n` be the number of nodes.

- Each node is visited a constant number of times across group discovery and reversal.
- Each pointer update is `O(1)`.

The running time is `O(n)`, and the auxiliary space is `O(1)`.

## Appendix

### Common Pitfalls
- Reversing the last partial group violates the contract; the stop condition must be checked before any rewiring begins.
- Losing `group_next` before reversal makes it impossible to reconnect the reversed block correctly.
