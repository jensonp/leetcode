---
description: Generate a Fundamentals/Appendix README.md for a LeetCode problem
globs:
  - README.md
---

# LeetCode README Workflow

Produce a README with two clearly separated parts:
- `## Fundamentals`
- `## Appendix`

`Fundamentals` is the canonical note.
`Appendix` is optional study support.

## Governing Rule

A section belongs in `Fundamentals` if removing it would weaken:
- the derivation of the algorithm,
- the correctness proof,
- or the complexity analysis.

A section belongs in `Appendix` if removing it would not weaken the proof, but would weaken:
- learning,
- recall,
- transfer,
- or usability.

## Non-Negotiable Principles

- `Fundamentals` must stand alone.
- `Appendix` must not introduce assumptions, proof obligations, or missing definitions that `Fundamentals` depends on.
- Do not mix interview coaching, motivational framing, or decorative walkthrough language into `Fundamentals`.
- Prefer one clear proof over repeated restatements of the same proof.
- Final code is optional and should appear only when the current task explicitly requests it.

## Required Structure

Use this shape by default.

# <problem number>: <title>

You may include one short metadata line or bullet list immediately under the title if it helps, but do not create extra top-level sections for packaging.

## Fundamentals

### Problem Contract
- Restate the problem precisely.
- Decode the input and output.
- State the assumptions the solution depends on.
- Explain why each important assumption matters.

### Definitions and State Model
- Define the variables, symbols, sets, pointers, windows, or recurrence terms used later.
- Keep equations small and purposeful.
- Every definition introduced here must be used later.

### Key Lemma / Invariant / Recurrence
- Isolate the exact statement that makes the algorithm valid.
- This is the mathematical center of the note.
- If the problem needs both a lemma and an invariant, state both here.

### Algorithm
- Give the final strategy step by step.
- Include pseudocode when it materially helps reconstruct the solution.
- Keep this section formal rather than motivational.

### Correctness Proof
- Prove the algorithm from the lemma, invariant, or recurrence above.
- Cover initialization, maintenance, and termination when the problem is iterative.
- Prove the exact claim needed for correctness; do not drift into stronger but unnecessary claims.

### Complexity Analysis
- Define the input size.
- Count the work per step.
- Bound the number of steps.
- State exact iteration counts when they matter.
- Distinguish worst-case, average-case, and best-case when relevant.

### Correctness-Sensitive Pitfalls
Include this subsection only if omitting it would make the formal argument incomplete or dangerously misleading.

## Appendix

`Appendix` is optional and modular, but the heading should still be present so the separation is explicit.
If there is nothing useful to add, write one short sentence saying no appendix material is needed.

Useful appendix subsections include:
- `### Worked Example`
- `### Visuals`
- `### Variants / Follow-Ups`
- `### Common Pitfalls`
- `### Implementation Notes`
- `### Interview Explanation`
- `### Self-Test Questions`
- `### Why Naive / Wrong Approaches Fail`
- `### Final Code` when explicitly requested

Only include the subsections that earn their place.

## Visual Policy

Visuals belong in `Appendix`, not in `Fundamentals`, unless the user explicitly asks for a visually-led note.

Rules:
- Visuals are optional by default.
- Add visuals only when they materially clarify geometry, pruning, state transitions, recursion structure, or invariants.
- For most problems, `0-3` visuals is enough.
- For genuinely visualization-heavy canonical problems, `3-6` visuals is the upper range.
- Do not require `10+` visuals.
- Do not treat visual count as a quality metric.
- Use local reproducible assets under `png/`, with generator code and `dot/` sources when the set is nontrivial.
- Do not rely on external hotlinked images for core teaching visuals.
- If visuals are present, audit them with `.agents/workflows/visual-image-audit.md`.

## Render Syntax Policy

README syntax must be GitHub-renderable.

Rules:
- Do not use raw LaTeX display delimiters such as `\[ ... \]` in Markdown prose.
- Prefer fenced `math` blocks for displayed equations.
- Keep inline notation in plain text or code spans unless the renderer is known to support the exact syntax being used.
- If a formula would render as literal control characters instead of math, rewrite it into a renderer-safe form.

## Quality Filter

Every paragraph in `Fundamentals` must do at least one of these:
- define the contract,
- define the state,
- state the key lemma or invariant,
- derive the algorithm,
- prove correctness,
- or justify complexity.

Everything else belongs in `Appendix` or should be cut.

## Disallowed

- Forcing packaging into `Fundamentals`.
- Requiring "What this teaches" style reflection in the core note.
- Requiring "Pattern visible", "Compressed Restatement", or "30-Second Interview Proof" inside the core note.
- Requiring "Next Step Before Coding" by default.
- Requiring "Clarifying Questions" unless the contract is genuinely ambiguous.
- Repeating the same lemma in multiple sections without adding new value.
- Treating a large visual count as proof of quality.
