# LeetCode Top Interview 150 — Study Strategy

## Objective

Become an elite software engineer. Not merely pass interviews.

The target is:

$$
\text{recognize} \rightarrow \text{derive} \rightarrow \text{justify} \rightarrow \text{implement} \rightarrow \text{perturb} \rightarrow \text{compress}
$$

Pattern study is necessary. Pure memorization is insufficient. The correct algorithmic progression is:

$$
\text{assisted comprehension} \rightarrow \text{independent reproduction} \rightarrow \text{reliable repetition} \rightarrow \text{fast production under variation}
$$

---

## Study Depth Policy

Not every problem deserves full rigor. The optimization objective is:

$$
\max \frac{\text{downstream transfer}}{\text{study time}}
$$

Formally, mark problem $p$ full-depth when:

$$
N(p) + C(p) + T(p) + B(p) - R(p)
$$

is high, where $N$ is new-pattern value, $C$ is proof-value, $T$ is transfer-value, $B$ is bug-surface, and $R$ is redundancy with patterns you already own. Difficulty alone is not the criterion.

### Full-depth (anchor problems)

Maximal rigor: full README following the workflow, split into `Fundamentals` and `Appendix`, with a formal proof in `Fundamentals` and visuals only when they materially help.

### Medium-depth

- Solve independently.
- Write a short formal proof sketch (invariant + termination + complexity).
- State exact time and space.
- Record one pitfall.
- Move on.

### Compressed (owned patterns)

Brief notes only. You already own the family.

### Progression rule

- Full rigor for the first 2–3 canonical problems in a new family.
- Medium-depth for the next few.
- Compressed notes after the family is owned.
- Exception: for DP, front-load state-definition problems before optimization-heavy or pattern-compression problems.

---

## Core Full-Depth Set (29 problems)

Study these at full rigor. Each is a canonical representative whose proof structure transfers broadly.

| # | Problem | Family | Why full-depth |
|---|---------|--------|----------------|
| 88 | Merge Sorted Array | In-place / basic two-pointers | Canonical loop-invariant reasoning for in-place backward merge |
| 11 | Container With Most Water | Two-pointers with elimination proof | Cleanest "move one pointer and prove why" argument |
| 15 | 3Sum | Sorted + two-pointers + dedup | Transfers to a large class of sorted-search problems |
| 42 | Trapping Rain Water | Two-pointers with maintained summary state | Strong invariant involving `left_max` / `right_max` |
| 55 | Jump Game | Greedy reachability | Minimal, canonical greedy feasibility proof |
| 134 | Gas Station | Greedy restart / prefix-deficit | Important proof style; many people memorize without understanding |
| 3 | Longest Substring Without Repeating Characters | Sliding window, fixed validity condition | Canonical variable-window state maintenance |
| 76 | Minimum Window Substring | Sliding window, hardest mainstream | Best representative for window validity accounting |
| 128 | Longest Consecutive Sequence | Hashing for linear-time existence | Teaches how to justify `O(n)` with a set instead of sorting |
| 73 | Set Matrix Zeroes | In-place matrix state encoding | Excellent for "reuse the input as metadata" |
| 56 | Merge Intervals | Sort-and-sweep interval invariant | Canonical interval merging schema |
| 138 | Copy List with Random Pointer | Pointer aliasing / structural copying | Good test of object identity versus value copying |
| 25 | Reverse Nodes in k-Group | Linked-list segment rewiring | High bug surface; teaches disciplined pointer surgery |
| 146 | LRU Cache | Design + data-structure invariants | One of the best design/invariant problems in the set |
| 98 | Validate Binary Search Tree | BST validity via range contracts | Essential recursive invariant pattern |
| 124 | Binary Tree Maximum Path Sum | Tree DP with local/global split | Canonical postorder DP on trees |
| 236 | Lowest Common Ancestor | Recursive return-contract reasoning | Excellent for reasoning about what recursion returns |
| 200 | Number of Islands | Graph traversal on grids | Canonical DFS/BFS visitation problem |
| 207 | Course Schedule | Cycle detection / DAG feasibility | Core graph reasoning via topo-sort or DFS colors |
| 127 | Word Ladder | BFS on implicit state graph | Canonical shortest-path-by-layers problem |
| 208 | Implement Trie | Trie as a data structure | Core prefix-tree design |
| 39 | Combination Sum | Backtracking search tree | Good canonical backtracking state model |
| 33 | Search in Rotated Sorted Array | Case-split binary search | Binary search when order is partially broken |
| 4 | Median of Two Sorted Arrays | Advanced binary-search partition proof | High-value proof problem; do not memorize blindly |
| 295 | Find Median from Data Stream | Heap invariant design | Canonical two-heap maintenance |
| 72 | Edit Distance | 2D alignment DP | First core DP anchor; forces exact prefix-state definition and base cases |
| 198 | House Robber | 1D DP recurrence | Best learned after formal state-definition discipline is in place |
| 322 | Coin Change | Unbounded-choice DP | Canonical objective-value DP; requires clear infeasible/base-state handling |
| 300 | Longest Increasing Subsequence | DP with structural optimization | Study after plain DP state design feels routine; forces `O(n²)` DP vs `O(n log n)` distinction |

---

## Conditional Full-Depth Set

Promote these to full-depth **only if** the corresponding family still feels weak after the core set.

| If this family is weak… | Promote these |
|-------------------------|---------------|
| Greedy | 45. Jump Game II, 135. Candy |
| Prefix/suffix scan | 238. Product of Array Except Self |
| Interval insertion/update | 57. Insert Interval, 452. Minimum Arrows to Burst Balloons |
| Stack / state machine | 71. Simplify Path, 224. Basic Calculator |
| Tree decomposition | 105. Construct BT from Preorder+Inorder, 114. Flatten BT to Linked List |
| Graph copying / boundary fill | 133. Clone Graph, 130. Surrounded Regions |
| Harder backtracking | 51. N-Queens, 79. Word Search, 212. Word Search II |
| DP state-definition / prefix-state | 139. Word Break, 97. Interleaving String |
| Stock-state DP | 123. Best Time to Buy/Sell Stock III or 188. IV |

---

## Dynamic Programming Study Order

Do not enter DP through optimization tricks. Enter through formal problem definition.

For the first few DP problems, the goal is not "spot the recurrence quickly." The goal is: define the subproblem so precisely that the recurrence becomes forced.

Use this order inside the DP family, regardless of whether each problem is being studied at full-depth or medium-depth under the global policy.

| Order | Problem | What it should teach |
|-------|---------|----------------------|
| 1 | 139. Word Break | `dp[i]` must be a formal statement about the prefix `s[0..i-1]`; ambiguity about index vs prefix-length is unacceptable |
| 2 | 72. Edit Distance | A DP state over two prefixes, plus exact base-row/base-column semantics |
| 3 | 97. Interleaving String | A 2D boolean state where each coordinate has a precise contract and the transition follows from the last consumed character |
| 4 | 198. House Robber | Once the state is defined correctly, the 1D recurrence is almost trivial |
| 5 | 322. Coin Change | Objective-value DP: define what is minimized, what counts as impossible, and how base states propagate |
| 6 | 123. Best Time to Buy/Sell Stock III or 188. IV | Explicit multi-state modeling: transaction count, holding status, and transition legality |
| 7 | 300. Longest Increasing Subsequence | Separate the baseline `O(n²)` DP definition from the later `O(n log n)` structural optimization |

DP-specific discipline:

- For problems 1-3, write the state definition before writing any recurrence.
- State whether indices denote positions or prefix lengths. Do not leave this implicit.
- State the base cases in words before encoding them in an array.
- For optimization problems, define the objective function formally: feasibility, minimum cost, maximum value, or count.
- Do not study LIS patience sorting until the `O(n²)` DP can be derived and justified cold.

---

## Per-Problem Workflow

1. **Extract the problem contract formally.** Define inputs, outputs, mutation rules, hidden assumptions.
2. **Blind attempt.** No LLM, no editorial reference.
3. **Write a formal solution draft before coding:**
   - State variables
   - Invariant or recurrence
   - Transition rule
   - Termination argument
   - Complexity derivation
4. **Implement from your own draft.** Not from a reference.
5. **Test edge cases.** The ones you identified in step 1.
6. **Write a short postmortem before seeking help.** What worked, what was unclear.
7. **Use LLM only as checker/auditor**, not primary author. Ask it to:
   - Find proof gaps
   - Challenge complexity claims
   - Generate counterexamples to wrong alternatives
   - Identify hidden assumptions
   - Test transfer with perturbations
8. **Reconstruct the final reasoning from memory.**

---

## LLM Prompt for Checker Mode

> For computer science and math topics, explain like a careful textbook author. Start from the formal definition, identify the variables, state what is being bounded or proved, and derive the result step by step. Distinguish exact values from asymptotic bounds, and worst-case from average-case or best-case. Do not use intuition-first paraphrases or simplifications unless I explicitly ask for intuition after the formal explanation.

---

## Pattern Ownership Status Labels

| Label | Meaning | What to do |
|-------|---------|------------|
| **N** | New — first encounter | Full-depth study |
| **E** | Early repetition — seen once, not owned | Solve again independently, compare |
| **C** | Consolidating — can derive but slowly | Timed practice, perturbation tests |
| **O** | Owned — fast cold derivation | Compressed notes, move on |

---

## Pattern Ownership Tests

You own a pattern when you can pass **all five**:

1. **Cold derivation after delay.** Restate contract, state variables, invariant, proof, code — from memory, after ≥24 hours.
2. **Whiteboard proof without code.** Prove correctness verbally with no implementation crutch.
3. **Variant/perturbation test.** Change one condition. Explain what breaks and what adapts.
4. **Time-bounded reimplementation.** Code the solution cleanly within interview time limits.
5. **Pattern articulation.** Explain the family, not just the problem. When does this pattern apply? What are the triggers?

---

## Mastery Model

Two layers. Both required.

**Layer 1 — Formal command.** You can derive the result step by step. Define input size, name the variable being counted, state the loop bound, distinguish worst-case from average-case.

**Layer 2 — Compression.** You can recognize the structure quickly and explain it economically without losing truth. Not simplified — compressed.

Training sequence: **formal first → restate precisely → test transfer → code and review.**

Derivation without recognition is inefficient. Recognition without derivation is unsafe. Both are required.

---

## Anti-Patterns to Avoid

- **Over-elaboration without compression.** If documentation length increases but cold derivation speed does not improve, the protocol is failing.
- **Passive consumption.** Re-reading verified LLM output is not studying. Independent reproduction of the reasoning chain is mandatory.
- **Memorizing without understanding.** High risk for: Gas Station, Median of Two Sorted Arrays, LIS patience sorting.
- **Full rigor on every problem.** Diminishing returns after the anchor is owned. Transition to medium-depth.
- **Using LLM as primary author.** Solve first. LLM audits second.

---

## Execution Schedule

1. **88. Merge Sorted Array** requires cold derivation test to transition from Status E to Status C.
2. Next core anchor: **11. Container With Most Water** (two-pointer elimination proof).
3. Execute the per-problem workflow.
4. Execute `/.agents/workflows/leetcode-problem.md` post-attempt.
5. Execute `/.agents/workflows/audit-readme.md`.
6. Execute `./audit.sh`.
7. Track Status N/E/C/O per family.
