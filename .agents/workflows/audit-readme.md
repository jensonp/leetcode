---
description: Audit a LeetCode README for Fundamentals/Appendix quality
---

# Audit LeetCode README

Review a generated README for formal quality, section discipline, and pedagogical boundary control.
For structural checks, run `./audit.sh <problem-dir>` first.

## Steps

1. Read `.agents/workflows/leetcode-problem.md`.
2. Read the target `README.md`.
3. Run `./audit.sh <problem-dir>`.
4. Run `.agents/workflows/visual-image-audit.md`. If the README embeds no local visuals, that is a failure under the current workflow.
5. Perform the checks below.

## Fundamentals Checks

### 1. Standalone Core Check
`Fundamentals` must stand on its own.

Fail if a reader must enter `Appendix` to recover:
- the problem contract,
- the key definition,
- the key lemma or invariant,
- the algorithm,
- the proof,
- or the complexity argument.

### 2. Formal Sufficiency Check
Check that `Fundamentals` contains:
- a precise contract,
- the variables or state model,
- the key lemma, invariant, or recurrence,
- the algorithm,
- the correctness proof,
- and the complexity analysis.

### 3. Undefined Terms Check
- Do not use technical terms before defining them.
- Define overloaded or easy-to-misread terms at first use.

### 4. Equation Translation Check
Every equation or symbolic statement in `Fundamentals` must be followed by:
- a plain-English translation,
- its purpose,
- and where it is used later.

### 5. Proof Discipline Check
The proof must:
- isolate the key claim explicitly,
- prove the exact claim needed for correctness,
- and avoid repeated restatements that add no new value.

### 6. Complexity Precision Check
Check that the note:
- defines the input size,
- counts the relevant work,
- separates exact counts from asymptotic bounds when relevant,
- and distinguishes worst-case, average-case, and best-case when relevant.

### 7. Render Syntax Check
Check that the README uses renderer-safe Markdown and math syntax.

Fail if:
- formulas are written with raw LaTeX display delimiters such as `\[ ... \]`,
- visible control syntax would leak into the rendered README,
- or section content relies on syntax that is unlikely to render correctly on GitHub.

### 8. Referential Clarity Check
In `Fundamentals`, explanatory sentences should bind directly to the symbols and objects under discussion.

Fail if:
- weak antecedents such as `the two chosen lines`, `the current pair`, `the shorter line`, or `the two lines` appear where direct symbolic reference would be clearer,
- descriptive fallback phrases such as `the lines at indices i and j` remain after `(i, j)` has already been introduced,
- prose discusses a formal object without attaching it to notation such as `(i, j)`, `H[i]`, `H[j]`, or `A(i,j)`,
- or a 2D container formulation uses `volume` where `area` is the correct model.

## Appendix Checks

### 9. Boundary Check
`Appendix` may improve learning, recall, or usability, but it must remain non-essential.

Fail if:
- `Appendix` introduces missing assumptions,
- `Appendix` carries the only statement of a proof-critical lemma,
- or `Appendix` quietly repairs an incomplete core argument.

### 10. Visual Presence And Necessity Check
Fail if:
- there is no `### Visuals` subsection,
- there are no embedded local visuals,
- visuals appear outside `Appendix`,
- visuals do not clarify a real confusion hotspot,
- or the note depends on visuals to repair an incomplete core argument.

### 11. Packaging Restraint Check
Fail if `Appendix` is bloated with material that does not improve:
- understanding,
- recall,
- transfer,
- or implementation safety.

## Final Reader Test

After one careful read of `Fundamentals` alone, the reader should be able to answer:
- What is the problem really asking?
- What is the key lemma, invariant, or recurrence?
- What is the algorithm?
- Why is it correct?
- Why is the complexity claim true?

`Appendix` should then help with:
- examples,
- visuals,
- variants,
- pitfalls,
- or implementation fluency.

## Output Format

Report findings as a table:

| Check | Pass/Fail | Issues Found |
|-------|-----------|--------------|
| Standalone Core | ✅/❌ | Missing proof-critical material from Fundamentals? |
| Formal Sufficiency | ✅/❌ | Which required core elements are missing or weak? |
| Undefined Terms | ✅/❌ | Terms used before definition |
| Equation Translation | ✅/❌ | Equations without translation or purpose |
| Proof Discipline | ✅/❌ | Weak lemma isolation or redundant restatements |
| Complexity Precision | ✅/❌ | Missing exactness, case distinctions, or counting logic |
| Render Syntax | ✅/❌ | Broken Markdown/math syntax or raw control delimiters |
| Referential Clarity | ✅/❌ | Weak antecedents or non-symbolic prose in Fundamentals |
| Appendix Boundary | ✅/❌ | Proof content leaking into Appendix |
| Visual Presence And Necessity | ✅/❌ | Missing visuals, decorative visuals, or core-dependent visuals |
| Packaging Restraint | ✅/❌ | Appendix bloat or filler |
| Final Reader Test | ✅/❌ | Which questions Fundamentals cannot answer |

Then list specific fixes needed, grouped by section.
