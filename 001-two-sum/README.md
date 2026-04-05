# 1: Two Sum

- **Difficulty:** Easy
- **Tags:** Array, Hash Table
- **Pattern:** Single-pass complement lookup

## Fundamentals

### Formal Statement of the Problem

Let $n \in \mathbb{N}$, where $\mathbb{N} = \{1, 2, 3, \dots\}$ denotes the set of positive integers. Let

$$
S = \langle s_0, s_1, \dots, s_{n-1} \rangle
$$

be a finite sequence of length $n$. The angle brackets $\langle \cdot \rangle$ denote an ordered sequence, so the order of the entries matters. For every index $k$, the symbol $s_k$ denotes the element of $S$ at position $k$.

Assume that every sequence value is an integer:

$$
s_k \in \mathbb{Z} \quad \text{for every } k.
$$

Here $\mathbb{Z} = \{\dots, -2, -1, 0, 1, 2, \dots\}$ denotes the set of all integers, and the symbol $\in$ means "is an element of."

Define the index set by

$$
I_n := \{0, 1, 2, \dots, n-1\}.
$$

The symbol $:=$ means "is defined to be." The braces $\{\cdot\}$ denote a set, and the symbol $\dots$ indicates continuation of the evident pattern.

Let $\tau \in \mathbb{Z}$ be the target sum. Define the candidate pair space by

$$
V := \{(i,j) \in I_n \times I_n \mid i < j\}.
$$

The notation $(i,j)$ denotes an ordered pair. The symbol $\times$ denotes Cartesian product, so $I_n \times I_n$ is the set of all ordered pairs of indices. The vertical bar $\mid$ means "such that." The inequality $i < j$ means that the first index is strictly smaller than the second. This excludes self-pairs and keeps exactly one ordering of each two-index choice.

Define the summation predicate $P$ by

$$
P(i,j) \iff s_i + s_j = \tau.
$$

The symbol $+$ denotes addition in the integers, the symbol $=$ denotes equality, and the symbol $\iff$ means "if and only if."

The objective is to compute the unique ordered pair $(i,j) \in V$ for which $P(i,j)$ is true. The uniqueness assumption may be written as

$$
\exists! (i,j) \in V \text{ such that } P(i,j).
$$

The symbol $\exists!$ means "there exists exactly one."

### Domain, Variables, Assumptions, and Constraint

**Domain.** Every sequence entry and the target lie in $\mathbb{Z}$. Every legal index lies in $I_n$. Every admissible output pair lies in $V$.

**Traversal Variables.** The symbol $k$ will denote the current index during a left-to-right scan. The symbol $u$ will denote an earlier index, meaning an index satisfying $u < k$.

**Baseline Search Space.** A brute-force algorithm checks the predicate $P(i,j)$ for every pair in $V$. If $A$ is a finite set, then $|A|$ denotes its cardinality, meaning its number of elements. Therefore

$$
|V| = \binom{n}{2} = \frac{n(n-1)}{2}.
$$

The symbol $\binom{n}{2}$ is read as "n choose 2." It denotes the number of two-element subsets of an $n$-element set. Thus the brute-force baseline examines a quadratic number of candidate pairs.

**Design Requirement.** The derivation must show how to replace the repeated scan over all earlier indices with one precise condition that can be checked directly at each step.

### Theorems and Proof Obligations

To avoid searching the entire previously processed portion of the sequence at every step, we must determine what value an earlier element would need in order to complete the target sum with the current element.

#### Lemma 1: Determinism of the Algebraic Complement

Fix an index $k \in I_n$. Let $u \in I_n$ satisfy $u < k$. Then

$$
P(u,k) \iff s_u + s_k = \tau.
$$

Because the integers are closed under subtraction, the expression $\tau - s_k$ is again an integer. Subtracting $s_k$ from both sides gives

$$
s_u = \tau - s_k.
$$

Here the symbol $-$ denotes subtraction in the integers.

Define the complement of the current value $s_k$ by

$$
c_k := \tau - s_k.
$$

The symbol $c_k$ is therefore not arbitrary. It is the unique integer that would have to appear earlier in the sequence in order to pair with $s_k$ and produce the target sum $\tau$.

#### Lemma 2: Prefix-Memory Equivalence

For each index $k \in I_n$, define the processed prefix by

$$
S_{\lt k} := \langle s_0, s_1, \dots, s_{k-1} \rangle.
$$

The subscript $\lt k$ means "strictly before index $k$."

Now introduce the data structure required by the process. A hash map is a structure that stores key-value associations. In this note, a key will be an integer value already seen in the sequence, and the associated value will be an index where that integer occurs.

Let $M$ denote such a hash map while the algorithm is processing index $k$. If an integer $x$ has already appeared in the prefix $S_{\lt k}$, then the map may store the key $x$ together with one earlier index $u < k$ satisfying $s_u = x$. The notation $M(x)$ means "the index stored in the map under the key $x$" when that key is present.

For the current index $k$, the statement "the key $c_k$ is present in $M$" is equivalent to the statement "there exists an index $u < k$ such that $s_u = c_k$." By Lemma 1, that is equivalent to saying that there exists an earlier index $u < k$ such that $P(u,k)$ is true.

#### Algorithmic Consequence

Lemma 1 reduces the search at index $k$ to one exact integer value, namely $c_k$. Lemma 2 shows that the remaining question is only whether that single value has already appeared in the processed prefix. The full scan over earlier indices is therefore unnecessary.

### Step-by-Step Derivation of the Algorithm

#### 1. State Initialization

Create an empty hash map $M$. At this moment no sequence value has been processed, so no key is stored.

#### 2. Domain Iteration

Traverse the index set $I_n$ in increasing order:

$$
k = 0, 1, 2, \dots, n-1.
$$

At the iteration indexed by $k$, the active sequence value is $s_k$.

#### 3. Complement Evaluation

Using Lemma 1, compute the exact integer value that would complete the target sum with $s_k$:

$$
c_k := \tau - s_k.
$$

#### 4. Membership Test and Return Rule

If the key $c_k$ is already present in $M$, then an earlier index storing the needed complement has already been found. In that case, return

$$
\bigl(M(c_k), k\bigr).
$$

This returned pair lies in $V$ because the stored index $M(c_k)$ comes from an earlier iteration and therefore satisfies $M(c_k) < k$.

#### 5. State Mutation

If the key $c_k$ is not present in $M$, then no earlier index pairs with $k$ to hit the target. The current value must therefore be recorded for later use. Write

$$
M(s_k) \gets k.
$$

The symbol $\gets$ means that the map is updated so that the key on the left stores the value on the right.

### Correctness Proof

We now prove that the algorithm returns the unique correct pair.

#### Loop Invariant

A loop invariant is a statement that is true before an iteration begins and remains true each time the loop advances.

Before the iteration for index $k$ begins, the map $M$ satisfies the following invariant:

For every integer value $x$, the key $x$ is present in $M$ if and only if there exists an index $u < k$ such that $s_u = x$. Whenever the key $x$ is present, the stored value $M(x)$ is one such earlier index $u$.

#### Initialization

Before the first iteration, one has $k = 0$. There is no index $u$ with $u < 0$, so no value has yet appeared in the processed prefix. The map was initialized as empty, so the invariant holds.

#### Maintenance

Assume that the invariant holds at the start of the iteration for some index $k$.

First compute the complement

$$
c_k = \tau - s_k.
$$

If the key $c_k$ is present in $M$, then by the invariant there exists an index $u < k$ such that $s_u = c_k$. Therefore

$$
s_u + s_k = c_k + s_k = (\tau - s_k) + s_k = \tau.
$$

Hence $P(u,k)$ is true, so returning the pair $\bigl(M(c_k), k\bigr)$ is correct.

If the key $c_k$ is not present in $M$, then no earlier index $u < k$ satisfies $s_u = c_k$. By Lemma 1, no earlier index forms a valid pair with $k$. The update

$$
M(s_k) \gets k
$$

then records the current value for later iterations. After this update, the invariant holds for the next iteration.

#### Termination

Let $(i^\ast, j^\ast)$ denote the unique solution pair in $V$. The superscript ${}^\ast$ is used only to mark these as the distinguished solution indices.

Because $i^\ast < j^\ast$, the iteration for index $i^\ast$ occurs before the iteration for index $j^\ast$. When the loop reaches $j^\ast$, the invariant implies that the key $s_{i^\ast}$ is already present in $M$. Since

$$
s_{i^\ast} + s_{j^\ast} = \tau,
$$

Lemma 1 gives

$$
s_{i^\ast} = \tau - s_{j^\ast} = c_{j^\ast}.
$$

Therefore the key $c_{j^\ast}$ is present in $M$ when index $j^\ast$ is processed, so the algorithm returns at that iteration. The returned pair is valid, and the uniqueness assumption forces it to be the unique desired answer.

This proves correctness.

### Complexity Claims

We now introduce the asymptotic notation required for the running-time and memory bounds.

Let $f$ and $g$ be numerical functions defined on $\mathbb{N}$ and taking nonnegative values. The statement $f(n) = O(g(n))$ means that there exist constants $C > 0$ and $n_0 \in \mathbb{N}$ such that

$$
f(n) \le Cg(n) \quad \text{for all } n \ge n_0.
$$

The statement $f(n) = \Theta(g(n))$ means that there exist constants $c_1 > 0$, $c_2 > 0$, and $n_0 \in \mathbb{N}$ such that

$$
c_1 g(n) \le f(n) \le c_2 g(n) \quad \text{for all } n \ge n_0.
$$

The phrase constant time means time bounded above by a fixed constant independent of $n$, which is written as $O(1)$.

The algorithm performs exactly one left-to-right traversal of the sequence, so it executes exactly $n$ iterations.

At each iteration it performs three kinds of work:

1. one subtraction to compute $c_k$,
2. one membership test in the hash map,
3. in the non-returning case, one insertion or update in the hash map.

The phrase expected time means average time under the probabilistic model used for hashing. The simple uniform hashing assumption says that keys behave as though they are distributed evenly among hash buckets. Under that assumption, membership tests and insertions in the hash map take expected constant time, that is, expected $O(1)$ time.

Therefore each iteration costs expected $O(1)$ time, and the full traversal costs expected

$$
\Theta(n).
$$

If many keys collide into the same bucket, individual map operations can degrade from constant time to linear time. In that worst case, the total running time can degrade to

$$
O(n^2).
$$

The phrase auxiliary space means memory used in addition to the input sequence and the returned pair. In the worst case, the map stores one entry for each processed sequence value before termination. Hence the auxiliary space is

$$
\Theta(n).
$$

### Conclusion

The brute-force formulation searches a quadratic pair space. The complement formulation collapses the question at index $k$ from "which earlier index works?" to "has the one required value $c_k$ already appeared?" The hash map implements that check directly, which yields a one-pass algorithm with expected linear running time and linear auxiliary space.
