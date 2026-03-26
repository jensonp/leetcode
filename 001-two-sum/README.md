# 1: Two Sum

- **Difficulty:** Easy
- **Tags:** Array, Hash Table
- **Pattern:** Single-pass complement lookup

## Fundamentals

### Foundational Definitions

We begin by fixing the notation that will be used throughout the note.

The symbol $\mathbb{Z}$ denotes the set of all integers:

$$
\mathbb{Z} = \{\dots, -2, -1, 0, 1, 2, \dots\}.
$$

The symbol $\mathbb{N}$ denotes the set of all positive integers:

$$
\mathbb{N} = \{1, 2, 3, \dots\}.
$$

The symbol $=$ denotes equality. The symbol $+$ denotes addition of integers. The symbol $-$ denotes subtraction of integers.

If $a \in \mathbb{Z}$ and $b \in \mathbb{Z}$, then both $a + b$ and $a - b$ are again elements of $\mathbb{Z}$. This closure under addition and subtraction is the algebraic fact that allows the complement expression $\tau - s_k$ to remain inside the same number system as the input.

A finite sequence of length $n$ is an ordered list of $n$ objects. The notation

$$
\langle s_0, s_1, \dots, s_{n-1} \rangle
$$

denotes a sequence whose first element is $s_0$, whose second element is $s_1$, and whose last element is $s_{n-1}$. The angle brackets $\langle \cdot \rangle$ indicate that order matters.

If $n \in \mathbb{N}$, then the symbol

$$
I_n := \{0, 1, 2, \dots, n-1\}
$$

denotes the index set of a sequence of length $n$. The symbol $:=$ means "is defined to be." The braces $\{\cdot\}$ denote a set.

If $A$ and $B$ are sets, then the Cartesian product $A \times B$ is the set of all ordered pairs $(a,b)$ with $a \in A$ and $b \in B$. The symbol $\in$ means "is an element of." The symbol $<$ means "is strictly less than." The symbol $\le$ means "is less than or equal to." The symbol $\ge$ means "is greater than or equal to." The symbol $\dots$ indicates continuation of the evident pattern.

If $A$ is a finite set, then $|A|$ denotes the number of elements in $A$. This number is called the cardinality of $A$.

The symbol

$$
\binom{n}{2}
$$

is the binomial coefficient "n choose 2." It denotes the number of two-element subsets of an $n$-element set, and it satisfies

$$
\binom{n}{2} = \frac{n(n-1)}{2}.
$$

In set-builder notation, the vertical bar $\mid$ means "such that." The symbol $\iff$ means "if and only if." The symbol $\exists!$ means "there exists exactly one."

Let $f$ and $g$ be numerical functions defined on $\mathbb{N}$ and taking nonnegative values. The statement $f(n) = O(g(n))$ means that there exist constants $C > 0$ and $n_0 \in \mathbb{N}$ such that

$$
f(n) \le Cg(n) \quad \text{for all } n \ge n_0.
$$

The statement $f(n) = \Omega(g(n))$ means that there exist constants $c > 0$ and $n_0 \in \mathbb{N}$ such that

$$
f(n) \ge cg(n) \quad \text{for all } n \ge n_0.
$$

The statement $f(n) = \Theta(g(n))$ means that both $f(n) = O(g(n))$ and $f(n) = \Omega(g(n))$ hold. Informally, $f(n) = \Theta(g(n))$ means that $f$ grows at the same asymptotic rate as $g$, up to constant factors.

The phrase constant time means running time bounded above by a fixed constant independent of $n$. In asymptotic notation, that is written as $O(1)$.

A hash map is a data structure that stores key-value associations. In this note, keys will be integer values already seen in the sequence, and values will be indices at which those integers occur. A membership test asks whether a given key is currently stored.

### Formal Statement of the Problem

Let $n \in \mathbb{N}$. Let

$$
S = \langle s_0, s_1, \dots, s_{n-1} \rangle
$$

be a finite sequence of length $n$ such that $s_k \in \mathbb{Z}$ for every index $k \in I_n$. Let $\tau \in \mathbb{Z}$ be the target sum.

Define the candidate pair space by

$$
V := \{(i,j) \in I_n \times I_n \mid i < j\}.
$$

This definition enforces two facts simultaneously. First, self-pairs are excluded because $i < j$ makes it impossible to have $i = j$. Second, each unordered pair of positions is represented exactly once, because either $i < j$ or $j < i$, but not both.

Define the summation predicate $P$ by

$$
P(i,j) \iff s_i + s_j = \tau.
$$

The objective is to compute the unique ordered pair $(i,j) \in V$ for which $P(i,j)$ is true. The uniqueness assumption may be written as

$$
\exists! (i,j) \in V \text{ such that } P(i,j).
$$

### Domain, Variables, Assumptions, and Constraints

**Domain.** Every sequence value lies in $\mathbb{Z}$, every index lies in $I_n$, and every admissible solution pair lies in $V$.

**Traversal Variables.** The symbol $k$ will denote the current index being processed during a left-to-right scan of the sequence. The symbol $u$ will denote an earlier index, meaning an index satisfying $u < k$.

**Combinatorial Baseline.** A brute-force search evaluates the predicate $P(i,j)$ for every pair $(i,j) \in V$. Since $|V| = \binom{n}{2} = n(n-1)/2$, the number of predicate evaluations is $\Theta(n^2)$.

**Design Requirement.** We seek an algorithm that avoids this quadratic enumeration and instead performs a single left-to-right traversal of the index set together with average constant-time map operations. Under that model, the intended running time is $\Theta(n)$.

### Theorems and Proof Obligations

To obtain linear running time, the algorithm must avoid comparing the current element $s_k$ against every earlier element $s_0, s_1, \dots, s_{k-1}$. The central question is therefore the following: for a fixed current index $k$, what exact value must an earlier element have in order to pair with $s_k$ and sum to $\tau$?

#### Lemma 1: Determinism of the Algebraic Complement

Fix an index $k \in I_n$. Let $u \in I_n$ satisfy $u < k$. Then

$$
P(u,k) \iff s_u + s_k = \tau.
$$

Because subtraction is valid inside $\mathbb{Z}$, subtracting $s_k$ from both sides yields

$$
s_u = \tau - s_k.
$$

Define the complement of the current value $s_k$ by

$$
c_k := \tau - s_k.
$$

The value $c_k$ is uniquely determined by $s_k$ and $\tau$. Therefore, for fixed $k$, an earlier index $u$ forms a valid pair with $k$ if and only if the earlier value is exactly $c_k$.

#### Lemma 2: Prefix-Memory Equivalence

For each index $k \in I_n$, define the processed prefix by

$$
S_{<k} := \langle s_0, s_1, \dots, s_{k-1} \rangle.
$$

The notation $<k$ in the subscript means "strictly before index $k$."

Let $M$ be a hash map with the following interpretation: if an integer value $x$ has already appeared in the prefix $S_{<k}$, then the map may store that key $x$ together with one index $u < k$ satisfying $s_u = x$. The notation $M(x)$ means the index stored under key $x$ when that key is present.

For the current index $k$, the statement "the key $c_k$ is present in $M$" is equivalent to the statement "there exists an earlier index $u < k$ such that $s_u = c_k$." By Lemma 1, this is in turn equivalent to the statement "there exists an earlier index $u < k$ such that $P(u,k)$ is true."

#### Algorithmic Consequence

Lemma 1 reduces the search for a partner of $s_k$ to the search for one specific value, namely $c_k$. Lemma 2 shows that a single membership test in a hash map is enough to decide whether that specific value already exists in the processed prefix. Hence the secondary scan over earlier indices can be eliminated.

### Step-by-Step Derivation of the Algorithm

#### 1. State Initialization

Create an empty hash map $M$. At this moment, no sequence value has yet been processed, so no key is present.

#### 2. Domain Iteration

Traverse the index set $I_n$ in increasing order:

$$
k = 0, 1, 2, \dots, n-1.
$$

At step $k$, the active sequence value is $s_k$.

#### 3. Complement Evaluation

Using Lemma 1, compute the unique value that would complete the target sum with $s_k$:

$$
c_k := \tau - s_k.
$$

#### 4. Membership Test and Return Rule

If the key $c_k$ is already present in $M$, then an earlier index storing the complement has already been seen. In that case, return the ordered pair

$$
\bigl(M(c_k), k\bigr).
$$

This returned pair belongs to $V$ because $M(c_k)$ is an earlier index and therefore satisfies $M(c_k) < k$.

#### 5. State Mutation

If the key $c_k$ is not present in $M$, then no earlier value forms a valid pair with $s_k$. The current value must therefore be recorded for use by later indices. Using the update arrow $\gets$, write

$$
M(s_k) \gets k.
$$

The symbol $\gets$ means that the map is updated so that the key on the left stores the value on the right.

### Correctness Proof

We now prove that the algorithm returns the unique correct pair.

#### Loop Invariant

Before the iteration for index $k$ begins, the map $M$ has the following property:

For every integer value $x$, the key $x$ is present in $M$ if and only if there exists an index $u < k$ such that $s_u = x$. Whenever the key $x$ is present, the stored value $M(x)$ is one such index $u$.

This statement is called a loop invariant because it is intended to remain true at the start of every loop iteration.

#### Initialization

Before the first iteration, one has $k = 0$. There is no index $u$ satisfying $u < 0$, so no value has occurred in the processed prefix. The map was initialized as empty, so the invariant holds.

#### Maintenance

Assume the invariant holds at the start of the iteration for some index $k$.

First compute $c_k = \tau - s_k$.

If the key $c_k$ is present in $M$, then by the invariant there exists an index $u < k$ such that $s_u = c_k$. By the definition of $c_k$, one has

$$
s_u + s_k = c_k + s_k = (\tau - s_k) + s_k = \tau.
$$

Hence $P(u,k)$ is true, and the algorithm returns the valid pair $(u,k)$. Since the actual returned first component is $M(c_k)$, and $M(c_k)$ is one such earlier index, the returned pair is correct.

If the key $c_k$ is not present in $M$, then no earlier index $u < k$ satisfies $s_u = c_k$. By Lemma 1, no earlier index forms a valid pair with $k$. The update

$$
M(s_k) \gets k
$$

then makes the current value available to later iterations. After this update, the invariant holds for the next iteration index $k+1$.

#### Termination

Let $(i^\ast, j^\ast)$ denote the unique pair in $V$ satisfying $P(i^\ast, j^\ast)$. The superscript ${}^\ast$ is used only to distinguish this specific solution pair from arbitrary indices.

Because $i^\ast < j^\ast$, the iteration processing index $i^\ast$ occurs before the iteration processing index $j^\ast$. When the algorithm reaches index $j^\ast$, the invariant implies that the key $s_{i^\ast}$ is already present in $M$. Since

$$
s_{i^\ast} + s_{j^\ast} = \tau,
$$

Lemma 1 gives

$$
s_{i^\ast} = \tau - s_{j^\ast} = c_{j^\ast}.
$$

Therefore the key $c_{j^\ast}$ is present in $M$ when index $j^\ast$ is processed, and the algorithm returns at that iteration. The returned pair is valid, and by the uniqueness assumption it must be the unique desired solution.

This proves that the algorithm is correct.

### Complexity Claims

We now justify the running-time and memory bounds.

The algorithm performs one left-to-right traversal of the sequence, so the loop executes exactly $n$ iterations.

During each iteration, the following work is performed:

1. one subtraction to compute $c_k$,
2. one hash-map membership test for the key $c_k$,
3. in the non-returning case, one hash-map insertion or update for the key $s_k$.

Under the simple uniform hashing assumption, the expected cost of a membership test and the expected cost of an insertion are both $O(1)$. Here "expected" means average over the hash-table behavior induced by the hashing rule, and "simple uniform hashing assumption" means that keys behave as though they are distributed evenly across hash buckets.

Since each of the $n$ iterations performs only expected constant-time work, the total expected running time is

$$
\Theta(n).
$$

If a pathological collision pattern causes many keys to fall into the same bucket, then individual map operations may degrade from constant time to linear time. In that worst case, the overall running time may degrade to

$$
O(n^2).
$$

The auxiliary space of an algorithm is the memory used in addition to the input sequence and the output pair. In the worst case, the algorithm stores one key-value entry for each processed element before returning. Therefore the auxiliary space usage is

$$
\Theta(n).
$$

### Conclusion

The brute-force formulation searches a quadratic pair space. The complement reformulation collapses the search at each index $k$ from "check all earlier indices" to "check whether one exact value $c_k$ has already appeared." A hash map realizes that check in expected constant time, which yields an expected $\Theta(n)$ algorithm with $\Theta(n)$ auxiliary space.
