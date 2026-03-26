# 1: Two Sum

- **Difficulty:** Easy
- **Tags:** Array, Hash Table
- **Pattern:** Complement lookup over a growing prefix

## Fundamentals

### Algebraic Foundations

We begin with the ambient algebraic language.

A **set** is a collection of objects. The symbol $R$ will denote a set.

A **binary operation** on $R$ is a rule that takes any ordered pair $(a,b)$ of elements of $R$ and returns another element of $R$. Here $a$ and $b$ are arbitrary elements of $R$, and the notation $(a,b)$ means that order matters: the first entry is $a$ and the second entry is $b$. We will write one binary operation as $+$ and another as $\cdot$.

The notation $(R,+)$ means the set $R$ together with the operation $+$. It is called a **group** if the following four properties hold.

**Group Property 1 (Closure).** For every $a \in R$ and every $b \in R$, the sum $a+b$ is again in $R$.

**Group Property 2 (Associativity).** For every $a,b,c \in R$, one has

$$
(a+b)+c = a+(b+c).
$$

**Group Property 3 (Identity Element).** There exists an element $0_R \in R$ such that, for every $a \in R$,

$$
a+0_R = a
\quad \text{and} \quad
0_R+a = a.
$$

The symbol $0_R$ denotes the identity element for addition on $R$.

**Group Property 4 (Inverse).** For every $a \in R$, there exists an element denoted by $-a$ such that

$$
a+(-a)=0_R
\quad \text{and} \quad
(-a)+a=0_R.
$$

The symbol $-a$ denotes the inverse of $a$ with respect to addition.

A group $(R,+)$ is called an **abelian group** if addition is also **commutative**, meaning that for every $a,b \in R$,

$$
a+b=b+a.
$$

A **ring** is a set $R$ equipped with two binary operations, written $+$ and $\cdot$, such that the following three properties hold.

**Ring Property 1.** The structure $(R,+)$ is an abelian group.

**Ring Property 2.** Multiplication is associative, meaning that for every $a,b,c \in R$,

$$
(a \cdot b) \cdot c = a \cdot (b \cdot c).
$$

**Ring Property 3.** Multiplication distributes over addition from both sides, meaning that for every $a,b,c \in R$,

$$
a \cdot (b+c) = a \cdot b + a \cdot c
\quad \text{and} \quad
(a+b) \cdot c = a \cdot c + b \cdot c.
$$

The symbol $\mathbb{Z}$ denotes the set of all integers:

$$
\mathbb{Z} = \{\dots,-2,-1,0,1,2,\dots\}.
$$

The symbol $\mathbb{N}$ denotes the set of positive integers:

$$
\mathbb{N} = \{1,2,3,\dots\}.
$$

The integers $\mathbb{Z}$ form a commutative ring with identity.

Here **commutative** means multiplication also satisfies

$$
a \cdot b = b \cdot a
\quad \text{for all } a,b \in \mathbb{Z}.
$$

Here **with identity** means there exists an integer written $1$ such that

$$
1 \cdot a = a \cdot 1 = a
\quad \text{for all } a \in \mathbb{Z}.
$$

For this problem, only the additive structure of $\mathbb{Z}$ will be used. Because every integer $a$ has additive inverse $-a$, subtraction is defined by

$$
\tau - a := \tau + (-a).
$$

Here the symbol $\tau$ denotes an integer, the symbol $a$ denotes an integer, and the symbol $:=$ means "is defined to be."

Therefore any equation of the form

$$
a+x=\tau
$$

can be rewritten by adding $-a$ to both sides, which gives

$$
x=\tau-a.
$$

This cancellation step is the algebraic fact needed later.

### Sequences and Indices

Let $n \in \mathbb{N}$ with $n \ge 2$. The symbol $n$ denotes the length of the input sequence. The symbol $\in$ means "is an element of," and the symbol $\ge$ means "is greater than or equal to."

Define the index set

$$
I_n := \{0,1,\dots,n-1\}.
$$

Here the braces $\{\ \}$ denote a set, and the notation $0,1,\dots,n-1$ means the consecutive integers from $0$ through $n-1$.

A **finite integer sequence of length $n$** is a function

$$
S : I_n \to \mathbb{Z}.
$$

The arrow $\to$ means "is a function from the set on the left to the set on the right." Thus the formula above says that each index in $I_n$ is assigned an integer value.

If $k \in I_n$, then $S(k)$ means the value of the function $S$ at the index $k$. We introduce the shorthand

$$
s_k := S(k).
$$

The subscript in $s_k$ records the index $k$; it is not an exponent.

Using that shorthand, we may write the sequence itself as

$$
\langle s_0, s_1, \dots, s_{n-1} \rangle.
$$

The angle brackets $\langle$ and $\rangle$ denote an ordered sequence.

If $A$ and $B$ are sets, then their **Cartesian product** $A \times B$ is the set of all ordered pairs $(a,b)$ with $a \in A$ and $b \in B$. The symbol $\times$ denotes this Cartesian product when it is used between sets.

Now define

$$
U_n := \{(i,j) \in I_n \times I_n \text{ such that } i < j\}.
$$

Here $i$ and $j$ denote indices, the symbol $<$ means "is strictly less than," and the phrase "such that" restricts the ordered pairs that are kept.

We use $U_n$ as the **candidate solution space**, meaning the set of all index pairs that are allowed to be returned. The symbol $\ne$ means "is not equal to." We require $i<j$, not merely $i \ne j$, because integer addition is commutative:

$$
s_i+s_j=s_j+s_i.
$$

Thus the ordered pairs $(i,j)$ and $(j,i)$ would encode the same unordered choice of two positions. Requiring $i<j$ keeps exactly one representative.

We write $|U_n|$ for the **cardinality** of $U_n$, meaning the number of elements of $U_n$.

We also write

$$
\binom{n}{2}
$$

for the **binomial coefficient** pronounced "n choose 2." It means the number of subsets with exactly $2$ elements that can be chosen from a set with exactly $n$ elements.

**Lemma.** The cardinality of $U_n$ is

$$
|U_n|=\binom{n}{2}.
$$

**Proof.** Choosing an element of $U_n$ is the same as choosing two distinct indices from the $n$ indices in $I_n$ and then writing them in increasing order. The number of such unordered two-element choices is $\binom{n}{2}$.

### Formal Problem Statement

Fix a target value $\tau \in \mathbb{Z}$. The symbol $\tau$ denotes the target sum.

Define a **predicate** $P(i,j)$ by

$$
P(i,j) \iff s_i+s_j=\tau.
$$

A predicate is a statement depending on variables that becomes either true or false after the variables are specified. The symbol $\iff$ means "if and only if": the statement on the left is true exactly when the statement on the right is true.

The task is to compute the unique pair $(i,j) \in U_n$ such that $P(i,j)$ is true. The symbol

$$
\exists!\,(i,j) \in U_n \text{ such that } s_i+s_j=\tau
$$

means "there exists exactly one pair $(i,j)$ in $U_n$ such that $s_i+s_j=\tau$."

A **brute-force** algorithm is one that checks every candidate directly. In this problem, brute force checks every pair in $U_n$, so it performs exactly $\binom{n}{2}$ pair checks.

### Deriving the Complement Condition

Fix an index $t \in I_n$. The symbol $t$ denotes the current right endpoint being examined.

We ask whether there exists an earlier index $u \in I_n$ with $u<t$ such that

$$
s_u+s_t=\tau.
$$

Here $u$ denotes a possible partner index for $t$.

Define the **complement** of $s_t$ relative to $\tau$ by

$$
c_t := \tau-s_t.
$$

The symbol $c_t$ denotes the exact integer value that would have to pair with $s_t$ in order to reach the target $\tau$.

**Lemma (Complement Lemma).** For every $u \in I_n$,

$$
s_u+s_t=\tau
\quad \Longleftrightarrow \quad
s_u=c_t.
$$

The symbol $\Longleftrightarrow$ also means "if and only if"; it is the display-math version of the same logical equivalence used above.

**Proof.** Starting from $s_u+s_t=\tau$, subtract $s_t$ from both sides. By the cancellation law established earlier,

$$
s_u=\tau-s_t=c_t.
$$

Conversely, if $s_u=c_t$, then

$$
s_u+s_t=(\tau-s_t)+s_t=\tau.
$$

This lemma turns the search at fixed $t$ into a **one-dimensional** membership question. Here "one-dimensional" means that once the index $t$ has been fixed, there is only one candidate value left to test, namely $c_t$.

### Data-Structural Reformulation

For the fixed index $t$, define

$$
S_{<t} := \{s_0,s_1,\dots,s_{t-1}\}.
$$

The subscript $<t$ means "coming from indices strictly smaller than $t$." Thus $S_{<t}$ is the set of values that appear before index $t$.

By the complement lemma, a valid pair ending at $t$ exists if and only if

$$
c_t \in S_{<t}.
$$

We therefore need a data structure that supports fast lookup of previously seen values. We use a **hash map**, meaning a data structure that stores **key-value pairs**: each key is associated with one stored value, and the structure is designed so that lookup and insertion are fast on average under standard hashing assumptions. A **lookup** asks whether a given key is already stored and, if it is stored, what value is attached to it. An **insertion** stores a new key together with its associated value.

Define

$$
M : \mathbb{Z} \rightharpoonup I_n.
$$

The symbol $\rightharpoonup$ means "partial function." A partial function from $\mathbb{Z}$ to $I_n$ assigns some integers a value in $I_n$, but it does not need to assign every integer such a value.

We write $\mathrm{dom}(M)$ for the **domain** of the partial function $M$, meaning the set of all integers $x$ for which $M(x)$ is defined. Thus

$$
x \in \mathrm{dom}(M)
\quad \Longleftrightarrow \quad
M(x) \text{ is defined}.
$$

Here $x$ denotes an arbitrary integer, and $M(x)$ denotes the value assigned by the map $M$ to the key $x$.

In this problem, the interpretation of $M$ is as follows: if a value $x$ has already appeared in the processed part of the sequence, then the map may store one earlier index where that value occurs. The map does not need to store every occurrence of $x$; one stored index is enough because the algorithm only needs to know whether some earlier occurrence exists.

A **membership test** is the act of checking whether a given key belongs to the current domain of the map. In this problem, the membership test is the question "is $c_t$ already in $\mathrm{dom}(M)$?"

### Algorithm

Before writing the algorithm, two remaining symbols must be fixed.

The symbol

$$
\varnothing
$$

denotes the **empty map**, meaning a map with no stored key-value pairs.

The symbol

$$
\gets
$$

denotes **assignment** or **update**. For example, $M(s_t) \gets t$ means "store the index $t$ under the key $s_t$ in the map $M$."

The word "Input" labels the data supplied to the algorithm before the algorithm starts.

The word "return" means terminate the algorithm and output the value that follows it.

The phrase

$$
\text{for } t = 0,1,\dots,n-1 \text{ do}
$$

means that the body of the loop is executed once for each listed value of $t$, in increasing order.

With all symbols defined, the one-pass algorithm is

$$
\begin{aligned}
&\text{Input: the sequence } \langle s_0,s_1,\dots,s_{n-1} \rangle \text{ and the target } \tau \\
&M \gets \varnothing \\
&\text{for } t = 0,1,\dots,n-1 \text{ do} \\
&\qquad c_t \gets \tau-s_t \\
&\qquad \text{if } c_t \in \mathrm{dom}(M) \text{ then return } (M(c_t),t) \\
&\qquad M(s_t) \gets t
\end{aligned}
$$

Because the loop processes indices in increasing order, every index already stored in $M$ is smaller than the current index $t$. Therefore any returned pair automatically satisfies the condition $i<j$.

### Correctness Proof

A **loop invariant** is a statement that is true before the first loop iteration and remains true after every iteration.

An **iteration** of the loop means one full execution of the loop body for one particular value of $t$.

**Theorem.** Under the uniqueness promise above, the algorithm returns exactly the unique pair $(i,j) \in U_n$ satisfying $s_i+s_j=\tau$.

**Proof.** After the algorithm has processed the indices $0,1,\dots,t-1$, and assuming the algorithm has not yet returned, we maintain the following loop invariant.

**Invariant 1.** For every integer $x$,

$$
x \in \mathrm{dom}(M)
\quad \Longleftrightarrow \quad
\text{there exists an index } k \in I_n \text{ with } k<t \text{ and } s_k=x.
$$

**Invariant 2.** If $x \in \mathrm{dom}(M)$, then $M(x)<t$ and $s_{M(x)}=x$.

**Invariant 3.** No valid solution pair lies entirely inside the prefix $\{0,1,\dots,t-1\}$.

The word **prefix** here means the already processed initial block of indices.

**Initialization.** When $t=0$, no indices have been processed, so $M$ is empty. Statement 1 holds because there are no seen values yet. Statement 2 holds because there is no integer $x$ for which $x \in \mathrm{dom}(M)$. Statement 3 holds because no pair can be formed from an empty prefix.

**Maintenance.** Assume the loop invariant holds at the start of iteration $t$. Compute $c_t=\tau-s_t$.

Case 1: $c_t \in \mathrm{dom}(M)$. By Statement 2, the index $u := M(c_t)$ satisfies $u<t$ and $s_u=c_t$. By the complement lemma,

$$
s_u+s_t=\tau.
$$

Hence $(u,t)$ is a valid pair in $U_n$. Because the problem promises uniqueness, $(u,t)$ must be the desired output, so returning it is correct.

Case 2: $c_t$ is not in $\mathrm{dom}(M)$. By Statement 1, there is no earlier index $u<t$ with $s_u=c_t$. By the complement lemma, there is no valid solution pair whose second index is $t$. The algorithm then updates the map by setting $M(s_t) \gets t$. After this update, Statement 1 remains true because the value $s_t$ has now been added to the processed prefix. Statement 2 remains true by construction of the update. Statement 3 remains true because it was already true at the start of the iteration and there is no solution ending at $t$.

**Termination.** Let $(i^\ast,j^\ast)$ denote the unique valid pair. The superscript $\ast$ marks these indices as the distinguished indices of the actual solution; it is not an exponent. Since $i^\ast<j^\ast$, the algorithm processes index $i^\ast$ before index $j^\ast$. When the loop reaches $t=j^\ast$, Statement 1 implies that $s_{i^\ast}$ is already recorded in $M$, so $s_{i^\ast} \in \mathrm{dom}(M)$. Because

$$
\tau-s_{j^\ast}=s_{i^\ast},
$$

we have $c_{j^\ast}=s_{i^\ast}$, so the algorithm returns $(i^\ast,j^\ast)$ at iteration $j^\ast$. Therefore the algorithm returns the unique correct answer.

### Complexity Analysis

We now define the asymptotic notation used in the complexity claims.

Let $f(n)$ and $g(n)$ be functions whose values are never negative.

We write

$$
f(n)=O(g(n))
$$

if there exist positive constants $C$ and $n_0$ such that

$$
f(n) \le Cg(n)
\quad \text{for every } n \ge n_0.
$$

The symbol $\le$ means "is less than or equal to." Here $C$ and $n_0$ are fixed positive real numbers that do not depend on $n$. The notation $O(g(n))$ means that $g(n)$ is an asymptotic upper bound for $f(n)$.

We write

$$
f(n)=\Theta(g(n))
$$

if there exist positive constants $c_1$, $c_2$, and $n_0$ such that

$$
c_1 g(n) \le f(n) \le c_2 g(n)
\quad \text{for every } n \ge n_0.
$$

Here $c_1$, $c_2$, and $n_0$ are again fixed positive real numbers that do not depend on $n$. The notation $\Theta(g(n))$ means that $g(n)$ is both an asymptotic upper bound and an asymptotic lower bound for $f(n)$.

The phrase **constant time** means time bounded above by a fixed constant independent of $n$; in asymptotic notation this is $\Theta(1)$. The phrase **expected time** means the average running time under the probability model supplied by the hashing assumption below. The phrase **worst-case** means the maximum running time over all inputs of the same length together with all collision behaviors allowed by the model. The phrase **auxiliary space** means the memory used by the algorithm besides the memory already occupied by the input sequence itself.

The **simple uniform hashing assumption** is the standard idealized assumption that keys behave as if they are spread evenly by the hash function, so lookup and insertion have constant expected time. A **pathological collision pattern** is an extremely bad hashing outcome in which many keys are sent to the same storage location, which makes map operations much slower.

**Theorem.** Under the simple uniform hashing assumption, the algorithm runs in expected time $\Theta(n)$ and uses auxiliary space $\Theta(n)$.

**Proof.** The loop performs exactly $n$ iterations, one for each index in $I_n$. In each iteration, the algorithm does one subtraction, one membership test in the hash map, and at most one insertion into the hash map. The subtraction takes constant time, which means it takes time $\Theta(1)$. Under the simple uniform hashing assumption, the membership test and the insertion each take constant expected time, which means expected time $\Theta(1)$. Therefore each iteration takes expected time $\Theta(1)$, and $n$ iterations together give total expected running time $\Theta(n)$.

For space, the map stores at most one earlier index for each processed value. In the worst case, the algorithm finds the unique solution only after it has already stored $n-1$ indices. Thus the extra memory used by the map grows linearly with $n$, so the auxiliary space is $\Theta(n)$.

If pathological collisions occur, hash-map operations need not remain constant-time on average. In that situation the running time can degrade to $O(n^2)$.

### Conclusion

The improvement over searching all $\binom{n}{2}$ candidate pairs comes from an algebraic identity, not from guesswork. Once $s_t$ is fixed, the equation $s_u+s_t=\tau$ determines exactly one required partner value, namely $c_t=\tau-s_t$. The algorithm stores earlier values in a hash map and tests whether that one required value has already appeared. That is why a single left-to-right pass through the sequence is enough.
