---
description: Generate a full interview-prep README for a LeetCode problem
---

---
description: Generate rigorous LeetCode README.md files that teach contract, reasoning, proof, and implementation mapping
globs:
  - README.md
---

# LeetCode README Super-Guide Standard

Your role is to produce a README that functions as a reusable interview-prep study guide.

The goal is not merely to solve the problem. The goal is to help the reader:
- understand the problem contract,
- recognize the pattern,
- compare alternatives,
- justify the final approach,
- prove correctness,
- and implement independently.

Optimize for clarity, correctness, and teachability.

## Non-Negotiable Principles

- Explain the problem contract before the algorithm.
- Define technical terms before relying on them.
- Every important constraint must be followed by:
  - **Why it matters**
  - **What design consequence follows**
- Show the reasoning ladder:
  - naive
  - refined
  - optimal
- Use the lightest proof style that makes correctness precise.
- Explicitly bridge abstraction levels:
  - contract
  - example
  - state model / equations
  - pseudocode
  - implementation notes
  - final code only if the current task explicitly requests code
- Prefer fewer high-value visuals and questions over broad filler.
- Do not announce a result before earning it. Build up: observation → consequence → conclusion. If a complexity claim, design choice, or key insight appears, the preceding sentences must make it feel inevitable, not surprising. Reasoning before headline.

## Required README Structure

Use these exact headings in this exact order.

# Problem Metadata
- LeetCode Number
- Difficulty
- Topic Tags
- Primary Pattern
- Secondary Pattern
- Why Interviewers Ask This

# Problem Contract & Hidden Semantics
- Restate the problem in plain English.
- Explain what the input and output really mean.
- Separate physical representation from logical data when relevant.
- Explain mutation rules, return behavior, ordering rules, duplicates, bounds, and space expectations.
- Surface hidden assumptions.
- For every important statement, explicitly add:
  - **Why it matters**
  - **This means for the solution**

Do not merely state facts like “the function returns void” or “the array is pre-allocated.”
Always explain the consequence for the algorithm.

# Conceptual Glossary
Define only the terms that matter for this problem, in simple language.

Possible examples:
- in-place
- auxiliary space
- pre-allocated capacity
- valid prefix / valid suffix
- non-decreasing
- invariant
- recurrence
- greedy choice
- pruning
- read-head
- write-head

Rules:
- Do not use loaded jargon before defining it.
- Keep definitions short and tied to this problem.

# Worked Example by Hand
- Use one concrete example before abstract reasoning.
- Show the state evolution step by step in a table.
- Include the key variables / pointers / state components.
- End with a short paragraph:
  - what the example teaches
  - what pattern becomes visible

# Clarifying Questions
List realistic questions a strong candidate should ask before solving.

Focus on:
- mutation rules
- duplicates
- ordering guarantees
- allowed extra space
- edge assumptions
- bounds
- whether inputs may be empty
- whether stability matters, if relevant

# Alternative Approaches & Tradeoffs
For each plausible approach, include:
- **Idea**
- **Why it seems reasonable**
- **Why a smart candidate might try it first**
- **Where it breaks down or underperforms**
- **Counterexample or limiting case**, when useful
- **Missing insight** that leads to a stronger approach

Required progression:
1. most naive or brute-force
2. meaningful intermediate refinement(s), if any
3. the point where the optimal idea becomes clear

Do not dismiss weaker approaches in one sentence.

# Core Insight
- State the one key idea that unlocks the best solution.
- Explain it once in plain English.
- Explain it once in precise technical language.

This section should feel like the “turning point” of the solution.

# Formal State Model
Define the formal objects before using them.

Possible contents:
- symbols
- indices
- pointers
- recurrence terms
- sets / intervals / windows
- invariants-to-be-proved

Rules:
- Keep equations small and purposeful.
- Every symbol must be defined.
- After each equation block, translate it into English.
- Do not add formalism that is not later used in the proof or pseudocode.

# Optimal Approach
Explain the final strategy step by step.

For each major step, answer both:
- **What happens**
- **Why this step is safe / valid / necessary**

The explanation should sound like something a strong candidate could say aloud in an interview.

# Correctness Proof
Use the proof style that best fits the problem family.

## For iterative / pointer / loop-based problems
Include:
- **Main invariant or core claim**
- **Initialization**
- **Maintenance**
- **Termination**
- **Final conclusion**

## For recursive / tree / divide-and-conquer / DP problems
Include:
- **Subproblem definition**
- **Base case**
- **Recurrence / decomposition**
- **Why all cases are covered**
- **Why combining subresults is correct**

## For greedy problems
Include:
- **Greedy choice**
- **Why the choice is safe**
- **Exchange argument or stays-ahead argument**
- **Why repeating the choice yields a global optimum**

## For graph / search / pruning problems
Include:
- **What state space is being explored**
- **Why no valid answer is missed**
- **Why pruning / visited-state logic is sound**
- **Why termination yields the desired answer**

Rules:
- Do not fake mathematical rigor.
- Use the simplest proof that makes the reasoning precise.
- End with a short subsection:
  - **30-Second Interview Proof**
  - This should summarize the correctness argument in concise spoken language.

# Equation → Pseudocode → Implementation Mapping
Bridge the idea across levels of abstraction.

Required flow:
1. state variables / equations
2. transition rules or recurrence
3. loop guard / branching logic / base cases
4. pseudocode
5. implementation notes

For each major line or branch in the pseudocode, explain:
- what it corresponds to in the math / state model
- why it exists
- what bug it prevents

If the current task explicitly requests final code:
- add final code after this section
- keep variable names aligned with the state model when reasonable
- briefly annotate how the code instantiates the pseudocode

If the current task does not request final code:
- stop at pseudocode and implementation notes

# Visualizing the Algorithm
Include 3-6 visuals only if each teaches something distinct.

Possible purposes:
- problem layout / data model
- why the naive approach wastes work
- pointer or state movement
- invariant preservation
- recurrence tree or DP table evolution
- edge-case behavior
- failure mode of a weaker approach

Rules:
- Every visual needs:
  - a title
  - 1-2 sentences introducing what it shows
  - 1-2 sentences interpreting why it matters
- Diagrams must explain, not decorate.
- Stop adding visuals once they stop adding new insight.

# Complexity Analysis
- State time complexity.
- State space complexity.
- Justify both from the structure of the algorithm.
- Compare with rejected approaches when useful.
- If asymptotic optimality matters, say why a better bound is impossible or unlikely.

# Edge Cases & Pitfalls
For each case, include:
- **Case**
- **Why it matters**
- **What the algorithm does**
- **Common implementation bug**

Focus on:
- empty inputs
- single-element cases
- duplicates
- boundary indices
- mutation hazards
- off-by-one errors
- exhausted pointers / windows / recursion edges

# Transferable Pattern Recognition
- Name the core pattern.
- List recognition triggers.
- Explain why this problem fits the pattern.
- Mention nearby problem shapes or sister problems.

This section should help the reader spot the pattern in a new problem later.

# Problem Variations & Follow-Ups
For each realistic variation, include:
- **What changes**
- **What stays the same**
- **Whether the same proof idea still works**
- **Whether complexity changes**
- **What new failure mode appears**

Prioritize realistic interviewer follow-ups over random extensions.

# Interview Simulation Questions

## Clarifying Questions I Should Ask
Questions the candidate should ask before solving.

## In-Problem Follow-Ups
Questions the interviewer may ask while the candidate is solving.

## Post-Solution Probes
Questions the interviewer may ask after the solution is explained.

Rules:
- Keep questions specific to the actual problem and pattern.
- Do not generate generic filler.

# Self-Test Questions
Provide 3-7 questions that test:
- contract understanding
- pattern recognition
- proof understanding
- edge-case handling
- ability to reconstruct the algorithm from memory

# Next Step Before Coding
State exactly what the reader should do next.

Good examples:
- hand-trace one more case from memory
- restate the invariant without notes
- rewrite the pseudocode from scratch
- explain why the rejected approach fails
- then implement the solution independently

## Quality Filter
Keep material only if it helps the reader do at least one of these:
- understand the contract
- reject a weaker approach
- see the key insight
- prove correctness
- avoid an implementation bug
- answer a realistic interviewer follow-up

Delete or compress anything that does not clear this bar.

## Disallowed Behavior
- Do not state facts without explaining why they matter.
- Do not use unexplained jargon.
- Do not jump from intuition to final answer without the missing bridge.
- Do not add equations that are never used later.
- Do not add visuals that do not teach a new idea.
- Do not include broad system-design or role questions unless they are tightly connected to the problem; if included, cap them at 3 and place them last.
- Do not let the README become a dump of facts. It must read like a coherent lesson.
- Do not announce conclusions before earning them (e.g., stating "O(m+n)" before explaining why). Build observation → consequence → conclusion chains so each sentence earns the next.

## Writing Standard
The tone must be:
- instructional
- rigorous
- practical
- interview-oriented
- easy to follow without dumbing down the logic

Every major section should help the reader answer one of these:
- What is the problem really asking?
- Why is this approach better than the obvious one?
- Why is it correct?
- How do I translate the idea into code?
- What would an interviewer ask next?