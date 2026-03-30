# Dynamic Programming Fundamentals

This note is about deriving dynamic programming solutions, not memorizing recurrences. The goal is to make the conversion

problem statement $\to$ state definition $\to$ recurrence $\to$ evaluation order $\to$ pseudocode

systematic.

---

## What Dynamic Programming Is

Dynamic programming is a method for evaluating a finite family of subproblems while reusing previously computed answers.

For a fixed input, a DP formulation consists of:

- a state space,
- an exact meaning for each state,
- base states,
- a recurrence that reduces larger states to smaller states,
- an order in which the recurrence can be evaluated.

In the most abstract form, DP defines a value function

$$
V : S \to C
$$

over a finite state space $S$, where each non-base state is computed from smaller states.

The crucial idea is not "fill an array." The crucial idea is:

- choose the right subproblem family,
- make the state exact,
- show the recurrence is exhaustive and legal,
- and evaluate states in a dependency-safe order.

---

## When DP Applies

Dynamic programming is appropriate when all of the following are true:

- the original problem can be decomposed into smaller subproblems,
- many larger subproblems depend on overlapping smaller subproblems,
- the future only depends on a compressed summary of the past,
- the dependency relation between states is acyclic or can be made acyclic.

If the future depends on information that the state does not store, the state is invalid.

If the subproblems do not overlap, plain recursion or divide-and-conquer may be enough.

If the state space is too large to enumerate, the formulation may be mathematically correct but algorithmically useless.

---

## Problem Types

Before defining the state, identify what kind of answer the problem asks for.

### Feasibility

The output asks whether something is possible.

$$
\text{value domain} = \{\mathrm{false}, \mathrm{true}\}
$$

Typical aggregator:

$$
\bigvee \quad \text{or} \quad \bigwedge
$$

Example: [139. Word Break](../139-word-break/README.md)

### Optimization

The output asks for the minimum or maximum value of some objective.

Typical aggregators:

$$
\min \quad \text{or} \quad \max
$$

Example: [198. House Robber](../198-house-robber/README.md), [72. Edit Distance](../072-edit-distance/README.md)

### Counting

The output asks for the number of admissible constructions.

Typical aggregator:

$$
\sum
$$

The recurrence must avoid double-counting and must specify exactly what is being counted.

---

## Core Workflow

Every DP derivation should follow the same pipeline.

### 1. State the original objective exactly

Write down:

- the input objects,
- the admissibility constraints,
- the required output,
- whether the question is feasibility, optimization, or counting.

### 2. Choose a subproblem family

Good DP states usually come from one of these axes:

- prefixes or suffixes,
- intervals,
- grid coordinates,
- index plus one extra resource or flag,
- tree nodes plus local context,
- subsets or bitmasks.

### 3. Define the state with exact semantics

Every state symbol must answer one unambiguous subproblem.

Bad:

- `dp[i]` means "best up to here somehow"

Good:

- `dp[i]` means "whether the prefix $s[0:i)$ is segmentable"
- `dp[i]` means "maximum money from the first $i$ houses"
- `dp[i][j]` means "minimum edit distance between $word1[0:i)$ and $word2[0:j)$"

### 4. Determine the legal state range

The table range comes from the state semantics, not from habit.

If the state is:

- prefix length $i$, then $i \in \{0,1,\dots,n\}$,
- array index $i$, then $i \in \{0,1,\dots,n-1\}$,
- interval endpoints $(l,r)$, then $0 \le l \le r < n$ or whatever the exact interval convention requires,
- grid prefixes $(i,j)$, then $(i,j) \in \{0,\dots,m\} \times \{0,\dots,n\}$ if prefix lengths are used.

### 5. Prove the base states

Base states are not placeholders. They are exact answers to degenerate subproblems.

Examples:

- empty prefix,
- first element only,
- zero budget,
- empty string versus nonempty string,
- leaf node,
- interval of length $1$.

### 6. Derive the recurrence from structure

Do not guess the recurrence. Derive it from the shape of a valid full solution.

Common derivation patterns:

- last decision,
- first decision,
- split point,
- include/exclude case split,
- local alignment of the last characters,
- choose one predecessor among legal predecessors.

### 7. Choose an evaluation order

Inspect the recurrence and write down which states a state depends on.

If every dependency is to a smaller state, tabulation is possible.

The evaluation order must be topological with respect to the dependency graph.

### 8. Translate quantifiers into loops

This is the step that converts mathematics into pseudocode.

- existence $\exists$ usually becomes a loop with an `if` and an early `break`,
- minimum or maximum becomes a loop maintaining a running best value,
- summation becomes an accumulator,
- conjunction over predecessors becomes a loop that may fail on one counterexample.

### 9. State the proof device

Most DP correctness proofs use:

- induction over state order,
- a table invariant,
- a lemma justifying the recurrence,
- or an exchange argument for a derived optimization recurrence.

### 10. Classify the complexity claim

State:

- the number of states,
- the number of transitions considered per state,
- the local cost of one transition,
- and the cost model for operations such as slicing or hashing.

The generic upper bound is:

$$
\text{time} \le \sum_{\text{states}} (\text{transitions per state}) \cdot (\text{local transition cost})
$$

---

## State Design Heuristics

### The state must contain all future-relevant information

If two histories can lead to different future possibilities, and the state merges them, then the state is missing information.

### Prefer the smallest state that is still correct

A state can fail in two ways:

- too small: it omits information needed for correctness,
- too large: it is correct but too expensive.

### Common state templates

- Prefix DP: "first $i$ items"
- Suffix DP: "from position $i$ onward"
- Interval DP: "subarray $[l,r]$"
- Grid DP: "first $i$ rows and $j$ columns" or cell $(i,j)$
- Index + resource: position plus budget, capacity, or remaining operations
- Index + mode: position plus holding flag, transaction count, parity, cooldown, and so on

### Prefix length versus array index

This distinction causes many off-by-one errors.

If the state means "the first $i$ items," then the natural range is:

$$
0,1,\dots,n
$$

If the state means "the item at position $i$," then the natural range is:

$$
0,1,\dots,n-1
$$

For problems built around cuts or prefixes, prefix-length states are usually cleaner.

---

## Exact Decomposition Versus Optimal Substructure

These are related but not identical.

### Exact decomposition

Used for feasibility and counting problems.

The recurrence must be both:

- complete: every valid full solution is represented by at least one recurrence branch,
- sound: every recurrence branch represents only valid full solutions.

### Optimal substructure

Used for minimization and maximization problems.

An optimal solution to a larger subproblem can be assembled from optimal solutions to smaller subproblems once the final decision is fixed.

In practice:

- `Word Break` relies on exact decomposition,
- `House Robber` relies on optimal substructure,
- `Edit Distance` uses a last-operation decomposition plus optimal substructure.

---

## Choosing the Evaluation Order

The recurrence tells you the dependency graph.

If the recurrence says that state $i$ depends only on states $j < i$, then the natural order

$$
0,1,2,\dots,n
$$

is valid.

If the recurrence says that state $(i,j)$ depends on:

$$
(i-1,j),\ (i,j-1),\ (i-1,j-1)
$$

then row-major or column-major order is valid.

If the recurrence says that interval $[l,r]$ depends on smaller intervals, then increasing interval length is often the right order.

The general rule is:

- write down the predecessors of a state,
- choose an order in which every predecessor appears earlier.

---

## From Recurrence to Pseudocode

This translation should feel mechanical once the recurrence is correct.

### Existence / feasibility

Mathematical form:

$$
dp[i] = \bigvee_{j<i} P(i,j)
$$

Pseudocode shape:

```text
dp[i] = false
for each predecessor j:
    if P(i, j):
        dp[i] = true
        break
```

### Minimization or maximization

Mathematical form:

$$
dp[i] = \min_{j<i} f(i,j)
\quad \text{or} \quad
dp[i] = \max_{j<i} f(i,j)
$$

Pseudocode shape:

```text
best = +infinity   # or -infinity for max
for each predecessor j:
    best = min(best, f(i, j))
dp[i] = best
```

### Counting

Mathematical form:

$$
dp[i] = \sum_{j<i} f(i,j)
$$

Pseudocode shape:

```text
dp[i] = 0
for each predecessor j:
    dp[i] += f(i, j)
```

---

## Correctness Proof Template

The default proof is induction in evaluation order.

### Step 1. State the meaning of the table

For every legal state $s$, state exactly what $dp[s]$ means.

### Step 2. Verify initialization

Show that each base state stores the correct answer to its subproblem.

### Step 3. Verify the update

Assume all predecessor states are correct. Then use the recurrence lemma to show the computed value for the current state is correct.

### Step 4. Extract the answer

Show that the returned state is exactly the original question.

For iterative DP, a useful invariant is:

- before computing the current state, every predecessor state already stores its correct value.

---

## Complexity Discipline

Never write a complexity claim without a cost model.

Count:

- number of states,
- number of transitions considered per state,
- cost of evaluating one transition.

Typical examples:

- `Word Break`: $O(n^2)$ transitions if substring access is treated as $O(1)$; otherwise slicing may push the bound to $O(n^3)$.
- `House Robber`: $n$ states and $O(1)$ work per state, so $O(n)$ time.
- `Edit Distance`: $(m+1)(n+1)$ states and $O(1)$ work per state, so $O(mn)$ time.

Auxiliary space is determined by:

- table size,
- memo table size,
- and extra data structures such as hash sets or transition caches.

---

## Memoization Versus Tabulation

Both implement the same recurrence.

### Memoization

- recursive,
- computes only reached states,
- often easier to derive first,
- may incur recursion overhead,
- requires care with recursion depth.

### Tabulation

- iterative,
- makes the evaluation order explicit,
- often easier to reason about space optimization,
- requires knowing a valid topological order.

If the state space is naturally rectangular or prefix-based, tabulation is often cleaner.

---

## Space Optimization

A full table is not always necessary.

If a state depends only on the previous $k$ layers, then often only those $k$ layers need to be stored.

Examples:

- `House Robber` depends only on the previous two prefix states,
- `Edit Distance` can be reduced from a full grid to a rolling row because each row depends only on the previous row and the current row's previous entry.

Space optimization is a second step. First derive the full correct DP. Then compress.

---

## Avoiding Formality Bloat

Formality becomes bloat when it does not strengthen correctness, eliminate ambiguity, or improve transfer.

Typical bloat:

- symbols introduced but never used,
- a fully quantified definition that never appears again in the proof,
- repeating the same claim in several notational forms,
- proving trivial facts that do not support the recurrence,
- expanding domain notation when no later argument depends on it.

The right standard is minimum sufficient formality.

For most interview-level DP problems, the formal core is:

- exact objective,
- exact state meaning,
- exact base cases,
- recurrence and why it is valid,
- evaluation order,
- correctness argument,
- complexity with cost model.

Any extra notation should justify itself.

---

## Interview Study Versus Research Preparation

### Interview-oriented study

The goal is fast exact derivation.

The learner should be able to say:

- what the state means,
- why the recurrence is exhaustive,
- why the evaluation order is valid,
- why the returned value answers the prompt,
- and what complexity is being claimed.

### Research-oriented preparation

The goal is stronger rigor and more general proofs.

It is often worth making explicit:

- the distinction between state space and search space,
- completeness and soundness of the recurrence separately,
- the bound type being claimed,
- all cost-model assumptions,
- and the precise abstraction that makes the state Markovian.

The same core applies in both settings; research simply expands the proof obligations.

---

## Worked Example 1: Word Break

Reference note: [139. Word Break](../139-word-break/README.md)

### Problem type

Feasibility.

### Lean formal core

Let $n = |s|$ and let $D$ be the set version of `wordDict`.

Define:

$$
dp[i] := \text{whether the prefix } s[0:i) \text{ is segmentable}
$$

with range:

$$
i \in \{0,1,\dots,n\}
$$

Base case:

$$
dp[0] = \mathrm{true}
$$

Recurrence:

$$
dp[i]
=
\bigvee_{j=0}^{i-1}
\bigl(dp[j] \land (s[j:i)\in D)\bigr)
$$

### Why the recurrence is correct

A nonempty segmented prefix must have a last word.

So:

$$
s[0:i) \text{ is segmentable }
\iff
\exists j < i \text{ such that } s[0:j) \text{ is segmentable and } s[j:i)\in D
$$

### Pseudocode

```text
D = set(wordDict)
n = len(s)
dp = [False] * (n + 1)
dp[0] = True

for i in range(1, n + 1):
    for j in range(i):
        if dp[j] and s[j:i] in D:
            dp[i] = True
            break

return dp[n]
```

### Evaluation order

State $i$ depends only on states $j < i$, so left-to-right prefix order is valid.

---

## Worked Example 2: House Robber

Reference note: [198. House Robber](../198-house-robber/README.md)

### Problem type

Maximization.

### Lean formal core

Let $n = |nums|$.

Define:

$$
dp[i] := \text{maximum money obtainable from the first } i \text{ houses}
$$

with range:

$$
i \in \{0,1,\dots,n\}
$$

Base cases:

$$
dp[0] = 0
$$

$$
dp[1] = nums[0]
$$

for $n \ge 1$.

Recurrence:

$$
dp[i] = \max \bigl(dp[i-1],\ dp[i-2] + nums[i-1]\bigr)
\qquad \text{for } i \ge 2
$$

### Why the recurrence is correct

For the first $i$ houses, there are exactly two legal cases:

- skip house $i-1$, yielding $dp[i-1]$,
- rob house $i-1$, forcing house $i-2$ to be skipped and yielding $dp[i-2] + nums[i-1]$.

These cases are exhaustive and mutually exclusive, so the optimum is their maximum.

### Pseudocode

```text
n = len(nums)
if n == 0:
    return 0

dp = [0] * (n + 1)
dp[1] = nums[0]

for i in range(2, n + 1):
    dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])

return dp[n]
```

### Space optimization

Only the previous two states are needed, so the table can be compressed to two rolling variables.

---

## Worked Example 3: Edit Distance

Reference note: [72. Edit Distance](../072-edit-distance/README.md)

### Problem type

Minimization.

### Lean formal core

Let $m = |word1|$ and $n = |word2|$.

Define:

$$
dp[i][j] := \text{minimum edit distance between } word1[0:i) \text{ and } word2[0:j)
$$

with range:

$$
(i,j) \in \{0,\dots,m\} \times \{0,\dots,n\}
$$

Base cases:

$$
dp[i][0] = i
$$

$$
dp[0][j] = j
$$

Recurrence:

If the last characters match:

$$
dp[i][j] = dp[i-1][j-1]
$$

Otherwise:

$$
dp[i][j] =
1 + \min\bigl(dp[i-1][j],\ dp[i][j-1],\ dp[i-1][j-1]\bigr)
$$

### Why the recurrence is correct

An optimal edit script ends with exactly one of:

- delete the last character of `word1`,
- insert the last character of `word2`,
- replace the last character of `word1`,
- or do nothing if the last characters already match.

### Pseudocode

```text
m = len(word1)
n = len(word2)
dp = [[0] * (n + 1) for _ in range(m + 1)]

for i in range(m + 1):
    dp[i][0] = i
for j in range(n + 1):
    dp[0][j] = j

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if word1[i - 1] == word2[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
        else:
            dp[i][j] = 1 + min(
                dp[i - 1][j],
                dp[i][j - 1],
                dp[i - 1][j - 1],
            )

return dp[m][n]
```

### Evaluation order

Each cell depends only on its upper, left, and upper-left neighbors, so row-major or column-major order is valid.

---

## Common Failure Modes

- The state omits information that affects future legality.
- The state range does not match the state semantics.
- Base cases are chosen by convenience instead of proof.
- The recurrence is plausible but not exhaustive.
- The recurrence uses illegal predecessors.
- The iteration order computes states before their predecessors.
- Complexity ignores local transition cost, especially slicing and substring creation.
- Space optimization is attempted before the full DP is fully understood.
- The learner memorizes the final recurrence without being able to reconstruct the state definition.

---

## A Compact DP Checklist

Before accepting a DP solution, verify all of the following:

- What kind of problem is this: feasibility, optimization, or counting?
- What exactly does each state mean?
- What are the legal values of the state variables?
- What are the base states, and why are they correct?
- Why does every valid solution correspond to recurrence branches?
- Why do recurrence branches correspond only to valid solutions?
- What smaller states does each state depend on?
- What evaluation order makes those predecessors available?
- What does the returned state represent?
- What is the time bound under the actual cost model?
- Can the space be reduced after correctness is established?

---

## Recommended Next Examples

After the three examples above, good follow-on problems are:

- [97. Interleaving String](../097-interleaving-string/README.md) for 2D Boolean DP,
- [322. Coin Change](../322-coin-change/README.md) for minimization with infeasible states,
- [300. Longest Increasing Subsequence](../300-longest-increasing-subsequence/README.md) for the distinction between a baseline DP and a later structural optimization.
