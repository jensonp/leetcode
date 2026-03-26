# 1: Two Sum

- **Difficulty:** Easy
- **Tags:** Array, Hash Table
- **Pattern:** Complement lookup over a growing prefix

## Fundamentals

### Algebraic and Combinatorial Preliminaries

**Definition (Ring).** A ring is a set $R$ equipped with two binary operations, addition and multiplication, such that:

1. $(R, +)$ is an abelian group.
2. Multiplication on $R$ is associative.
3. Multiplication distributes over addition from both sides.

The integers $\mathbb{Z}$ form a commutative ring with identity.

**Remark.** For this problem, only the additive structure of $\mathbb{Z}$ matters. Because $(\mathbb{Z}, +)$ is an abelian group, every integer has an additive inverse, subtraction is well-defined, and any equation of the form

$$
a + x = \tau
$$

may be rewritten uniquely as

$$
x = \tau - a.
$$

That cancellation law is the algebraic fact the algorithm depends on.

**Definition (Finite Integer Sequence).** Let $n \in \mathbb{N}$ with $n \ge 2$. A finite integer sequence of length $n$ is a function

$$
S : I_n \to \mathbb{Z},
\qquad
I_n := \{0,1,\dots,n-1\}.
$$

We write $S(k) = s_k$ and identify $S$ with the ordered list

$$
\langle s_0, s_1, \dots, s_{n-1} \rangle.
$$

**Definition (Cartesian Product).** If $A$ and $B$ are sets, then

$$
A \times B := \{(a,b) \mid a \in A,\ b \in B\}
$$

is their Cartesian product. Its elements are ordered pairs.

**Definition (Canonical Pair Space).** The candidate solution space is

$$
U_n := \{(i,j) \in I_n \times I_n \mid i < j\}.
$$

**Remark.** It is important to require $i < j$, not merely $i \ne j$. Since addition in $\mathbb{Z}$ is commutative,

$$
s_i + s_j = s_j + s_i,
$$

so $(i,j)$ and $(j,i)$ represent the same unordered solution. Restricting to $i < j$ removes this duplication and makes the uniqueness promise mathematically coherent.

**Lemma.** The cardinality of $U_n$ is

$$
|U_n| = \binom{n}{2}.
$$

**Proof.** Choosing an element of $U_n$ is equivalent to choosing an unordered two-element subset of $I_n$ and then writing it in increasing order. The number of such subsets is $\binom{n}{2}$.

### Formal Problem Statement

Fix a target value $\tau \in \mathbb{Z}$. Define the predicate

$$
P(i,j) \iff s_i + s_j = \tau,
\qquad (i,j) \in U_n.
$$

The problem is to compute the unique pair $(i,j) \in U_n$ such that $P(i,j)$ holds, under the promise

$$
\exists!\,(i,j) \in U_n \text{ such that } s_i + s_j = \tau.
$$

Here $\exists!$ means "there exists exactly one."

Brute force evaluates the predicate on every pair in $U_n$, so it performs $\binom{n}{2} = \Theta(n^2)$ checks. The objective is to derive an algorithm whose expected running time is linear in $n$.

### Deriving the Complement Condition

Fix an index $t \in I_n$. The question at time $t$ is whether there exists an earlier index $u < t$ such that

$$
s_u + s_t = \tau.
$$

At first glance this looks like a two-dimensional search over pairs of indices. The next lemma shows that once $t$ is fixed, the problem becomes one-dimensional.

**Lemma (Complement Lemma).** Define the complement of $s_t$ relative to $\tau$ by

$$
c_t := \tau - s_t.
$$

Then for every $u \in I_n$,

$$
s_u + s_t = \tau
\quad \Longleftrightarrow \quad
s_u = c_t.
$$

**Proof.** Starting from $s_u + s_t = \tau$, subtract $s_t$ from both sides:

$$
s_u = \tau - s_t = c_t.
$$

Conversely, if $s_u = c_t$, then

$$
s_u + s_t = (\tau - s_t) + s_t = \tau.
$$

**Consequence.** For a fixed right endpoint $t$, we do not need to search over all $u < t$. We only need to determine whether the specific value $c_t$ has already appeared among the previously processed elements.

### Data-Structural Reformulation

For each time $t$, define the prefix-value set

$$
S_{<t} := \{s_0, s_1, \dots, s_{t-1}\}.
$$

By the complement lemma, the instance at time $t$ is solved if and only if

$$
c_t \in S_{<t}.
$$

So the remaining problem is dynamic membership:

- Process the sequence from left to right.
- At each step, test whether the complement of the current value has already appeared.
- If not, record the current value for future steps.

To support this efficiently, maintain a hash map

$$
M : \mathbb{Z} \rightharpoonup I_n,
$$

meaning a finite partial function from integer values to indices. Its intended interpretation is

$$
x \in \mathrm{dom}(M)
\quad \Longleftrightarrow \quad
\text{some previously processed index stores the value } x.
$$

If $x \in \mathrm{dom}(M)$, then $M(x)$ is one such earlier index.

**Remark.** The map does not need to store every occurrence of a repeated value. It is enough to store one prior index for each value, because the complement test asks only whether such an index exists.

### Algorithm

Scan the sequence once from left to right.

$$
\begin{aligned}
&\text{Input: } \langle s_0, s_1, \dots, s_{n-1} \rangle,\ \tau \\
&M \gets \varnothing \\
&\text{for } t = 0,1,\dots,n-1 \text{ do} \\
&\qquad c_t \gets \tau - s_t \\
&\qquad \text{if } c_t \in \mathrm{dom}(M) \text{ then} \\
&\qquad\qquad \text{return } (M(c_t), t) \\
&\qquad M(s_t) \gets t
\end{aligned}
$$

Because the hash map contains only indices from earlier iterations, any returned pair automatically satisfies the canonical ordering $i < j$.

### Correctness Proof

**Theorem.** Under the promise that there exists a unique pair $(i,j) \in U_n$ satisfying $s_i + s_j = \tau$, the algorithm returns exactly that pair.

**Proof.** We use a loop invariant.

After processing indices $0,1,\dots,t-1$, and assuming the algorithm has not yet returned, the following statements hold:

1. For every integer $x$,
   $$
   x \in \mathrm{dom}(M)
   \quad \Longleftrightarrow \quad
   \exists k < t \text{ such that } s_k = x.
   $$
2. If $x \in \mathrm{dom}(M)$, then $M(x) < t$ and $s_{M(x)} = x$.
3. No solution pair lies entirely inside the prefix $\{0,1,\dots,t-1\}$.

**Initialization.** When $t = 0$, the map is empty. Statements (1) and (2) hold trivially because no indices have been processed. Statement (3) also holds trivially because no pair can be formed from the empty prefix.

**Maintenance.** Assume the invariant holds at the start of iteration $t$. Compute $c_t = \tau - s_t$.

Case 1: $c_t \in \mathrm{dom}(M)$.

By statement (2), the index $u := M(c_t)$ satisfies $u < t$ and $s_u = c_t$. By the complement lemma,

$$
s_u + s_t = \tau.
$$

Hence $(u,t) \in U_n$ is a valid solution pair. Because the problem promises uniqueness, this pair is exactly the desired answer.

Case 2: $c_t \notin \mathrm{dom}(M)$.

By statement (1), there is no prior index $u < t$ with $s_u = c_t$. By the complement lemma, no valid pair ending at $t$ exists. The algorithm then inserts $M(s_t) := t$. After this update, statements (1) and (2) remain true for the new prefix, and statement (3) remains true because there was no earlier solution by induction and no solution ending at $t$.

**Termination.** Let $(i^\ast, j^\ast)$ be the unique solution pair, with $i^\ast < j^\ast$. When the loop reaches iteration $t = j^\ast$, the index $i^\ast$ has already been processed. Therefore $s_{i^\ast} \in \mathrm{dom}(M)$, and since

$$
\tau - s_{j^\ast} = s_{i^\ast},
$$

the algorithm returns at iteration $j^\ast$. Thus it must terminate with the correct answer.

### Complexity Analysis

**Theorem.** Under the simple uniform hashing assumption, the algorithm runs in expected time $\Theta(n)$ and uses auxiliary space $\Theta(n)$.

**Proof.**

- The loop processes each index exactly once, so there are $n$ iterations.
- Each iteration performs one subtraction, one hash-table membership test or lookup, and at most one insertion.
- The subtraction is $\Theta(1)$.
- Under the simple uniform hashing assumption, lookup and insertion are expected $\Theta(1)$.

Therefore the total expected running time is

$$
n \cdot \Theta(1) = \Theta(n).
$$

For space usage, in the worst case the algorithm stores one entry for each processed value before discovering the solution. This is at most $n-1$ entries, so the auxiliary space is

$$
\Theta(n).
$$

**Remark.** If the hash function degenerates and causes pathological collisions, the constant-time expectation fails and the running time can degrade to $O(n^2)$. So the linear-time bound is an expected bound, not an unconditional worst-case guarantee for arbitrary hashing behavior.

### Conclusion

The improvement from quadratic search to linear expected time is not a heuristic trick. It follows directly from the algebraic identity

$$
s_u + s_t = \tau
\quad \Longleftrightarrow \quad
s_u = \tau - s_t,
$$

which reduces each step to a single membership query over previously seen values. A hash map answers that query in expected constant time, so a one-pass algorithm is sufficient.
