# Dynamic Programming Fundamentals

## Formal Statement of the Problem Class

Let \(X\) denote the set of valid inputs. For each input \(x \in X\), the objective is to compute an output \(F(x)\).

A dynamic programming formulation for input \(x\) consists of the following data:

- a finite state space \(S_x\),
- a distinguished initial state \(s_{\mathrm{start}}(x) \in S_x\),
- a base-state set \(B_x \subseteq S_x\),
- a strict well-founded order \(\prec_x\) on \(S_x\),
- for each non-base state \(s \in S_x \setminus B_x\), a finite decision set \(A_x(s)\),
- for each \(s \in S_x \setminus B_x\) and \(a \in A_x(s)\), a successor state \(T_x(s,a) \in S_x\) satisfying
  \[
  T_x(s,a) \prec_x s,
  \]
- a value domain \(C_x\),
- a base-value map \(b_x : B_x \to C_x\),
- and an evaluation rule for non-base states.

The value function is a map
\[
V_x : S_x \to C_x.
\]
It is defined by
\[
V_x(s) =
\begin{cases}
b_x(s), & s \in B_x, \\
\operatorname{Agg}_x\Bigl(\bigl(\Phi_x(s,a,V_x(T_x(s,a)))\bigr)_{a \in A_x(s)}\Bigr), & s \notin B_x.
\end{cases}
\]

The symbols \(\Phi_x\) and \(\operatorname{Agg}_x\) depend on the problem type.

- In a feasibility problem, \(C_x = \{\mathrm{false}, \mathrm{true}\}\), and \(\operatorname{Agg}_x\) is typically logical disjunction or conjunction.
- In a minimization problem, \(C_x\) is an ordered cost domain, and \(\operatorname{Agg}_x\) is \(\min\).
- In a maximization problem, \(C_x\) is an ordered value domain, and \(\operatorname{Agg}_x\) is \(\max\).
- In a counting problem, \(C_x = \mathbb{N}_0\), and \(\operatorname{Agg}_x\) is addition subject to the exact counting convention of the problem.

The computational objective is to evaluate \(V_x(s_{\mathrm{start}}(x))\), or more generally an explicitly specified extraction function of the state values.

---

## Domain, Variables, Assumptions, Constraints, Search Space, and State Space

### Domain

The input domain is the set \(X\) of valid instances. Every symbol used in the formulation must be typed precisely:

- input objects belong to their stated domains,
- state identifiers belong to \(S_x\),
- state values belong to \(C_x\),
- and decisions belong to the finite sets \(A_x(s)\).

### Variables

The principal variables are:

- \(x\): the original input,
- \(s\): a state in \(S_x\),
- \(a\): a legal decision from state \(s\),
- \(T_x(s,a)\): the successor state after decision \(a\),
- \(V_x(s)\): the exact value attached to state \(s\).

### Assumptions and Constraints

The formulation must specify all structural assumptions needed for correctness:

- finiteness of the state space,
- legality conditions for transitions,
- whether repeated states may occur in the naive search,
- whether the dependency relation is acyclic,
- and whether local operations such as substring extraction, hash lookup, or table access are treated as constant-time, logarithmic-time, or linear-time operations.

Complexity claims are invalid unless the underlying cost model is stated.

### Search Space

For each state \(s\), let \(\Omega_x(s)\) denote the set of admissible complete solutions extending from that state.

Depending on the problem class, the quantity of interest may be:

- the predicate \(\Omega_x(s) \neq \varnothing\),
- the minimum of a cost functional over \(\Omega_x(s)\),
- the maximum of a value functional over \(\Omega_x(s)\),
- or the cardinality \(|\Omega_x(s)|\).

The search space concerns complete admissible solutions.

### State Space

The state space \(S_x\) is not the set of complete solutions. It is the set of subproblems chosen so that:

- each state has exact semantics,
- different solution paths that produce the same residual subproblem map to the same state,
- and the value of a state depends only on that state, not on the history used to reach it, unless that history has been encoded into the state itself.

If the value of a subproblem depends on information omitted from the state representation, the formulation is incorrect.

---

## Formal Statement of the Definition

A problem admits a dynamic programming formulation if there exists a tuple
\[
\mathcal{D}_x =
\bigl(S_x, s_{\mathrm{start}}(x), B_x, \prec_x, A_x, T_x, C_x, b_x, \Phi_x, \operatorname{Agg}_x\bigr)
\]
such that the following conditions hold.

### 1. Exact State Semantics

For every state \(s \in S_x\), there is a formally stated subproblem \(P_x(s)\). The value \(V_x(s)\) must mean exactly one quantity attached to \(P_x(s)\). Typical examples include:

- a feasibility predicate,
- a minimum cost,
- a maximum attainable value,
- or a count of admissible constructions.

No symbol such as \(dp[i]\) or \(dp[i][j]\) may be used before the meaning of the indices has been fixed precisely.

### 2. Exact Base-State Semantics

For every base state \(s \in B_x\), the value \(b_x(s)\) must be proved correct directly from the problem definition.

### 3. Exact Decomposition

For every non-base state \(s\), each admissible complete solution in \(\Omega_x(s)\) must determine at least one legal first decision \(a \in A_x(s)\) and a residual admissible complete solution in \(\Omega_x(T_x(s,a))\).

This is the completeness direction of the recurrence derivation.

### 4. Exact Reconstruction

For every non-base state \(s\) and every legal decision \(a \in A_x(s)\), any admissible residual solution in \(\Omega_x(T_x(s,a))\) must combine with \(a\) to produce an admissible complete solution in \(\Omega_x(s)\) with the value prescribed by \(\Phi_x\).

This is the soundness direction of the recurrence derivation.

### 5. Acyclic Dependence

For every dependency \(T_x(s,a)\), one has \(T_x(s,a) \prec_x s\). Therefore the recurrence is well-founded, and the state values can be evaluated in an order compatible with \(\prec_x\).

### 6. Correct Answer Extraction

The answer required by the original problem must be shown to equal the extracted value from the designated start state.

Dynamic programming is therefore not the assertion that a recurrence exists. It is the claim that an exact value function over an explicitly defined state space can be evaluated by reusing subproblem values along an acyclic dependency structure.

---

## Derivation of Properties and Proof Obligations

Any complete dynamic programming solution note must discharge the following obligations.

### Obligation 1: Formal Statement of the Original Problem

State the input, output, admissibility conditions, and objective function or predicate exactly.

Examples:

- feasibility: prove whether an admissible construction exists,
- optimization: minimize or maximize a formally specified quantity,
- counting: count the admissible constructions under an exact counting convention.

### Obligation 2: State Definition

Define the state variables with exact semantics.

This includes:

- whether an index denotes a position, a prefix length, an interval boundary, a transaction count, a bitmask, or another object,
- what quantity is stored at each state,
- and what information has been deliberately excluded from the state.

If the problem uses prefixes, the distinction between the index set \(\{0,\dots,n-1\}\) and the prefix-length set \(\{0,\dots,n\}\) must be made explicit.

### Obligation 3: Base States

Prove the base states from the original problem definition. Base states are not placeholders. They are exact values of degenerate subproblems.

### Obligation 4: Recurrence Derivation

Derive the recurrence from a structural decomposition of admissible solutions.

For each non-base state, prove:

- completeness: every admissible full solution is represented by at least one recurrence branch,
- soundness: every recurrence branch constructs only admissible full solutions,
- and if the branches are aggregated by \(\min\), \(\max\), logical disjunction, or addition, that aggregation matches the objective exactly.

### Obligation 5: Evaluation Order

Prove that every dependency points to a strictly smaller state under a well-founded order. This justifies recursive memoization or iterative tabulation in a topological order.

### Obligation 6: Correctness of the Algorithm

State the invariant, induction hypothesis, lemma, exchange argument, monotonicity property, or other proof device used by the algorithm.

Then show that:

- initialization is correct,
- every state update preserves the claimed meaning of the table or memoized map,
- and the final returned value is the original objective.

### Obligation 7: Complexity Classification

Complexity statements must identify the bound type and cost model.

If each state is evaluated once, the worst-case asymptotic upper bound is
\[
O\!\left(\sum_{s \in S_x} \sum_{a \in A_x(s)} c_x(s,a)\right),
\]
where \(c_x(s,a)\) is the cost of evaluating one transition, including all local work such as substring checks, hash lookups, arithmetic, or comparisons.

The auxiliary-space upper bound is
\[
O\!\left(|S_x| + \text{representation cost of input-derived structures}\right).
\]

These are upper bounds, not automatically tight bounds. A tight bound requires a matching lower bound or an exact count under the same cost model.

---

## Minimal Checklist for a DP Note

- Formal statement of the problem.
- Domain, variables, assumptions, and state space.
- Exact definition of every state symbol.
- Base cases proved from the definition.
- Recurrence derived with soundness and completeness.
- Evaluation order justified by a well-founded dependency relation.
- Correctness proof tied to the actual algorithm.
- Complexity claim labeled by bound type and cost model.
