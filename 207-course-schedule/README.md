# 207: Course Schedule

- **Difficulty:** Medium
- **Tags:** Graph, Topological Sort
- **Pattern:** DAG feasibility via indegrees

## Fundamentals

### Problem Contract
There are `numCourses` vertices `0 .. numCourses-1`. Each prerequisite pair `[a, b]` means a directed edge `b -> a`. Return whether every course can be completed, which is equivalent to asking whether the graph is acyclic.

### Definitions and State Model
For each vertex `v`, let `indegree[v]` be the number of incoming edges not yet removed. Maintain a queue of all vertices whose current indegree is `0`.

Kahn's algorithm repeatedly removes a zero-indegree vertex and deletes its outgoing edges.

### Key Lemma / Invariant / Recurrence
#### Zero-Indegree Lemma
In any finite directed acyclic graph, at least one vertex has indegree `0`.

#### Removal Invariant
After removing some set of vertices by Kahn's algorithm, the remaining graph has exactly the remaining edges, and the queue contains precisely the remaining vertices whose indegree is `0` in that graph.

If the process ever stops with unremoved vertices, then every remaining vertex has indegree at least `1`, which implies a directed cycle in the remaining finite graph.

### Algorithm
1. Build adjacency lists and indegrees.
2. Initialize the queue with all indegree-`0` vertices.
3. Pop vertices from the queue, counting how many are removed.
4. For each outgoing edge `u -> v`, decrement `indegree[v]`; if it becomes `0`, enqueue `v`.
5. Return whether the removed count equals `numCourses`.

```text
build adj and indegree
queue = all v with indegree[v] == 0
seen = 0
while queue not empty:
    u = pop queue
    seen += 1
    for v in adj[u]:
        indegree[v] -= 1
        if indegree[v] == 0:
            push v
return seen == numCourses
```

### Correctness Proof
By the zero-indegree lemma, every acyclic remaining graph always offers at least one vertex that can legally be taken next. The removal invariant shows that Kahn's algorithm tracks exactly those legal next choices.

If the algorithm removes all `numCourses` vertices, then it has produced a topological order, so the graph is acyclic and every course can be completed.

If the algorithm stops early, the queue is empty while vertices remain. By the invariant, every remaining vertex has indegree at least `1` within the remaining graph. In a finite graph this implies a cycle, because following incoming edges indefinitely must revisit a vertex. A cycle makes completion impossible. Therefore the algorithm returns `true` exactly when all courses can be finished.

### Complexity Analysis
Let `V = numCourses` and `E = number of prerequisite pairs`.

- Building the graph costs `O(V + E)`.
- Each vertex enters and leaves the queue at most once.
- Each edge is processed once when its tail is removed.

The running time is `O(V + E)`, and the auxiliary space is `O(V + E)`.

## Appendix

### Common Pitfalls
- Reversing the edge direction changes the indegree semantics and breaks the proof.
- A successful DFS from one vertex does not imply global feasibility; cycles may exist in a disconnected component.
