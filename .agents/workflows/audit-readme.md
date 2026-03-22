---
description: Audit a LeetCode README for teaching quality and comprehension
---

# Audit LeetCode README

Review a generated README for comprehension quality, not just structural compliance. (For structural checks, run `./audit.sh <problem-dir>` first.)

## Steps

1. **Read the rules.** Read `.cursor/rules/leetcode_study_workflow.mdc` for the required section structure.
   If the README contains local visuals, also read `.agents/workflows/visual-image-audit.md`.

2. **Read the target README.** Read the `README.md` in the specified problem directory.

3. **Run the structural audit first.** Run `./audit.sh <problem-dir>` and confirm all headings pass. If not, fix structure before auditing content.

4. **Audit the visuals if present.** Confirm the image set has already passed the per-image audit in `.agents/workflows/visual-image-audit.md`. If not, do that before signing off.
   If the audit reveals an obvious mechanical defect with a clear fix, do not stop at the finding. Fix it, regenerate the assets, and rerun the image audit before continuing.

5. **Perform the Comprehension Audit below.**

---

## Comprehension Audit
Before finalizing the README, perform a full readability and teaching pass.

For every major section, check all of the following:

### 1. Undefined Terms Check
- Do not use technical terms before they are defined.
- If a term is easy to misuse or easy to gloss over, define it in plain English at first use.
- Examples:
  - in-place
  - auxiliary space
  - pre-allocated capacity
  - invariant
  - pruning
  - recurrence
  - monotonic
  - valid prefix / suffix

### 2. Why-It-Matters Check
Every important statement must answer:
- **What does this mean?**
- **Why does it matter?**
- **What consequence does it have for the solution?**

Bad:
- "The function returns void."
Good:
- "The function returns void, so we are not allowed to build and return a separate answer. The merged result must be written back into the provided data structure."

Bad:
- "nums1 is pre-allocated."
Good:
- "nums1 has physical space for `m + n` elements, but only the first `m` are valid input. The remaining `n` positions are writable capacity reserved for the merge."

### 3. Equation Translation Check
Every equation, symbolic definition, or formal statement must be followed by:
- a plain-English translation,
- the exact intuition it captures,
- and where it will be used later.

Do not include equations that are not used in the proof, pseudocode, or implementation notes.

### 4. Bridge Check
Do not jump directly between abstraction levels.

Always bridge in this order:
- concrete example
- general idea
- formal state / equations
- pseudocode
- implementation notes
- final code only if requested

If any section skips a level, add the missing bridge.

### 5. Proof Readability Check
The correctness proof must not merely be correct; it must also be teachable.

After the full proof, include:
- a short plain-English proof summary,
- and a **30-Second Interview Explanation** that a candidate could actually say aloud.

### 6. Pseudocode Alignment Check
Every major pseudocode branch or loop must map back to:
- a variable from the state model,
- a proof idea,
- or a specific edge case.

If a line of pseudocode exists but its purpose is not explained, explain it.

### 7. Confusion Hotspot Check
Look for sentences likely to confuse a learner because they are:
- compressed,
- jargon-heavy,
- technically true but not illuminating,
- or missing assumptions.

Rewrite those sentences with:
- simpler wording,
- one concrete example,
- and an explicit consequence.

### 8. Filler Removal Check
Delete or compress material that does not help the reader do one of these:
- understand the contract,
- choose among approaches,
- prove correctness,
- map reasoning into code,
- avoid a bug,
- answer a likely follow-up.

If a paragraph sounds impressive but does not improve understanding, cut it.

### 9. Final Reader Test
The README should allow the reader to answer all of these after one careful read:
- What is the problem really asking?
- Why is the obvious approach weaker?
- What is the key insight?
- Why is the final approach correct?
- How do the equations map to pseudocode?
- What would be easy to mess up in implementation?

---

## Output Format

Report findings as a table per check:

| Check | Pass/Fail | Issues Found |
|-------|-----------|--------------|
| Undefined Terms | ✅/❌ | List any terms used before defined |
| Why-It-Matters | ✅/❌ | List bare statements missing consequences |
| Equation Translation | ✅/❌ | List equations without English follow-up |
| Bridge Check | ✅/❌ | List abstraction jumps |
| Proof Readability | ✅/❌ | Missing plain summary or 30-sec explanation? |
| Pseudocode Alignment | ✅/❌ | Unmapped lines? |
| Confusion Hotspots | ✅/❌ | List confusing sentences |
| Filler Removal | ✅/❌ | List paragraphs that don't serve the 5 purposes |
| Final Reader Test | ✅/❌ | Which questions can't be answered? |

Then list specific fixes needed, grouped by section.
