---
description: Audit a LeetCode README against the interview-prep standard
---

# Audit LeetCode README

Review a generated README for compliance with the interview-prep standard.

## Steps

1. **Read the rules.** Read `.cursor/rules/leetcode_study_workflow.mdc` for the required section structure.

2. **Read the target README.** Read the `README.md` in the specified problem directory.

3. **Structural check.** Verify these exact headings exist in this exact order:
   - `# Problem Metadata`
   - `# Problem Contract & Hidden Semantics`
   - `# Worked Example by Hand`
   - `# Clarifying Questions`
   - `# Alternative Approaches & Tradeoffs`
   - `# Core Insight`
   - `# Formal State Model`
   - `# Correctness Proof`
   - `# Equation → Pseudocode → Code Mapping`
   - `# Visualizing the Algorithm`
   - `# Complexity Analysis`
   - `# Edge Cases & Pitfalls`
   - `# Transferable Pattern Recognition`
   - `# Problem Variations & Follow-Ups`
   - `# Interview Questions`
   - `# Self-Test Questions`
   - `# Next Step Before Coding`

   Report any missing or out-of-order headings.

4. **Content quality check.** For each section, verify:
   - **Contract:** Does it decode physical vs logical meaning? Does it explain what the return type implies?
   - **Worked Example:** Is there a full trace table (not just prose)?
   - **Alternatives:** Does each rejected approach have a counterexample and a "missing insight"?
   - **Core Insight:** Is it ≤3 sentences and speakable aloud?
   - **Proof:** Are there three separate claims (invariant, safety, termination)? Does safety include algebra?
   - **Mapping:** Does it bridge equations to pseudocode with English explanations per branch?
   - **Visuals:** Are there ≥4 diagrams? Does each have an intro sentence and interpretation?
   - **Interview Qs:** Are they relevant to the problem's actual difficulty level (no drifting into systems design for an Easy)?

5. **Quality filter.** Flag any paragraph that does not help:
   - understand the contract,
   - reject a bad approach,
   - prove the algorithm,
   - write the code,
   - or answer a realistic follow-up.

6. **Report.** Output a summary table:

   | Section | Present | Quality | Issue |
   |---------|---------|---------|-------|
   | ...     | ✅/❌   | Strong/Weak/Missing | Description |

   Then list specific fixes needed.
