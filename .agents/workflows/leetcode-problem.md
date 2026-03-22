---
description: Generate a proof-first README.md for a LeetCode problem
globs:
  - README.md
---

# LeetCode README Workflow

Produce a README that works as a canonical reference first and a study aid second.
The note should feel rigorous, compact, and reusable. It should not read like interview-coaching filler wrapped around a correct idea.

## Goal

Help the reader:
- understand the exact contract,
- see why weaker approaches fail,
- isolate the key lemma,
- prove the final algorithm,
- and reconstruct the implementation from the proof.

## Non-Negotiable Principles

- Explain the contract before the algorithm.
- Use one concrete example before abstract proof.
- Isolate the exact lemma or invariant that justifies the final move.
- Prefer one clear proof over several rhetorical restatements of the same proof.
- Include final code only if the current task explicitly asks for it.
- Keep visuals lean and proof-serving.

## Core README Structure

Use these exact core headings in this exact order.

# Problem Metadata
- LeetCode Number
- Difficulty
- Topic Tags
- Primary Pattern
- Secondary Pattern
- Why Interviewers Ask This

# Problem Contract & Hidden Semantics
- Restate the problem precisely.
- Decode what the input and output mean.
- State the assumptions the solution depends on.
- For each important statement, say why it matters for the design.

# Worked Example by Hand
- Trace one concrete example step by step.
- Show the evolving state in a table when helpful.
- End with at most one short sentence if the example exposes the key lemma.

# Alternative Approaches & Tradeoffs
For each plausible rejected approach:
- state the idea,
- explain why a smart reader might try it,
- identify the exact flaw or cost,
- and name the missing insight.

Required progression:
1. naive or brute force
2. meaningful refinement, if one exists
3. point where the optimal idea becomes inevitable

If no meaningful intermediate refinement exists, say so directly.

# Core Insight
- State the one key observation that unlocks the solution.
- Then isolate the exact lemma or safety claim that makes the move valid.

# Formal State Model
- Define the symbols used later.
- Keep equations small and purposeful.
- After each equation block, translate it into English.
- Do not introduce formalism that is not later used.

# Optimal Approach
- Explain the final algorithm step by step.
- For each step, answer both:
  - what happens
  - why that step is safe or necessary

# Correctness Proof
- Use the lightest proof style that makes the reasoning precise.
- For iterative problems, cover initialization, maintenance, and termination.
- For greedy or pruning problems, isolate the safe-discard or exchange argument explicitly.
- Prove the claim actually needed for correctness; do not drift into stronger but irrelevant statements.

# Equation -> Pseudocode -> Implementation Mapping
Bridge the proof to the implementation:
1. restate the state variables or equation,
2. translate the transition rule,
3. write pseudocode,
4. explain the bug-prone branches and loop guards.

If the current task explicitly requests final code:
- add it after this section,
- keep names aligned with the state model when practical.

# Visualizing the Algorithm
Adhere to `.cursor/rules/visual_organization.mdc`.

Rules:
- Use only the visuals needed to make the proof and state transitions easy to follow.
- For many problems, 3-6 visuals is enough.
- Add another image only when a real confusion hotspot remains.
- Prefer local reproducible assets under `png/`, with generator code and `dot/` sources when the set is nontrivial.
- Do not rely on external hotlinked images for the core lesson.
- After rendering, formally audit every embedded image with `.agents/workflows/visual-image-audit.md`.
- If the image audit finds an obvious mechanical issue with a clear fix path, fix it, regenerate, and re-audit in the same pass.

# Complexity Analysis
Derive the complexity formally:
1. define the input size,
2. count work per iteration,
3. bound the number of iterations,
4. state the case being analyzed,
5. conclude time and space.

Avoid decorative compressed restatements when the derivation already says everything needed.

# Edge Cases & Pitfalls
Record only cases that matter to the proof or implementation.

For each important case, include:
- what the case is,
- why it matters,
- what the algorithm does,
- and the common bug if one exists.

# Problem Variations & Follow-Ups
Limit to realistic extensions.

For each variation, state:
- what changes,
- what stays the same,
- whether the same proof survives,
- and whether the complexity changes.

## Optional Appendices

Add these only when they add distinct value and do not dilute the main proof spine:
- `# Conceptual Glossary`
- `# Clarifying Questions`
- `# What Breaks If`
- `# Transferable Pattern Recognition`
- `# Interview Questions`
- `# Interview Simulation Questions`
- `# Self-Test Questions`
- `# Next Step Before Coding`

If an optional section mostly repeats earlier content in softer language, omit it.

## Quality Filter

Every paragraph must do at least one of these:
- define the contract,
- reject a weaker approach,
- isolate the key lemma,
- prove correctness,
- map proof to implementation,
- warn about a realistic bug,
- or handle a realistic variation.

If it does none of those, cut it.

## Writing Standard

The tone should be:
- rigorous,
- compact,
- practical,
- and easy to follow.

The README should read like a coherent mathematical note with implementation consequences, not like a motivational walkthrough.
