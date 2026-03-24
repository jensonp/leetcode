# 146: LRU Cache

- **Difficulty:** Medium
- **Tags:** Hash Table, Linked List, Design
- **Pattern:** Indexed doubly linked list with eviction invariant

## Fundamentals

### Problem Contract
Implement a cache with capacity `C` supporting `get(key)` and `put(key, value)` in `O(1)` average time. When capacity is exceeded, evict the least recently used entry.

Recency is updated by every successful `get` and every `put` of an existing key.

### Definitions and State Model
Use:
- a hash map `M` from keys to nodes,
- a doubly linked list ordered from most recently used near the head sentinel to least recently used near the tail sentinel.

Each node stores `(key, value)` so eviction can remove the node from both structures.

### Key Lemma / Invariant / Recurrence
#### Representation Invariant
At all times:
- `M` contains exactly the keys currently in the cache,
- every node in the list except sentinels appears in `M`,
- the list order is recency order, with the least recently used node adjacent to the tail sentinel.

#### Constant-Time Update Lemma
Given a node pointer, removing it from the doubly linked list and reinserting it immediately after the head sentinel both take `O(1)` time. The hash map supplies that node pointer in `O(1)` average time.

### Algorithm
- `get(key)`: if `key` is absent, return `-1`; otherwise move its node to the front and return its value.
- `put(key, value)`: if `key` exists, update its value and move its node to the front. If `key` is new, insert a new front node, record it in `M`, and if size exceeds `C`, remove the node before the tail sentinel and delete its key from `M`.

```text
get(key):
    if key not in M: return -1
    node = M[key]
    remove(node)
    insert_after_head(node)
    return node.value

put(key, value):
    if key in M:
        node = M[key]
        node.value = value
        remove(node)
        insert_after_head(node)
    else:
        node = new Node(key, value)
        M[key] = node
        insert_after_head(node)
        if size(M) > C:
            victim = tail.prev
            remove(victim)
            delete M[victim.key]
```

### Correctness Proof
The representation invariant is true initially for the empty cache.

For `get(key)`, an absent key correctly yields `-1`. If `key` is present, the constant-time update lemma moves its node to the front, so the list order again matches recency after the access. The map still points to the same node, so the invariant is preserved.

For `put(key, value)`, updating an existing key changes only its value and recency position, preserving membership and order. Inserting a new key adds it to both `M` and the front of the list, marking it as most recent. If capacity is exceeded, the victim at `tail.prev` is exactly the least recently used entry by the invariant, so evicting it is correct. Thus every operation preserves the invariant, and every eviction removes precisely the least recently used key.

### Complexity Analysis
Let `C` be the cache capacity.

- Hash-map lookup, insert, and delete are `O(1)` average time.
- Doubly linked list removal and insertion are `O(1)`.

So both `get` and `put` run in `O(1)` average time. The space usage is `O(C)` for the map and list nodes.

## Appendix

### Common Pitfalls
- Using a singly linked list makes middle-node removal non-constant unless a predecessor map is added, which complicates the invariant.
- Storing only values in the list is insufficient because eviction must also remove the corresponding hash-map entry by key.
