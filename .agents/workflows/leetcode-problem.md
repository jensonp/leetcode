---
description: Generate a full interview-prep README for a LeetCode problem
---

# LeetCode Problem README Generation

Given a LeetCode problem link, generate a complete interview-prep README following the semantic ladder.

## Steps

1. **Read the workflow rules.** Read `.cursor/rules/leetcode_study_workflow.mdc` for the full required section structure before generating anything.

2. **Create the problem directory.** Name it `{number}-{slug}` (e.g., `088-merge-sorted-array`). Create it inside `~/leetcode/`.

3. **Phase 1 — Contract.** Write only:
   - Problem Metadata
   - Problem Contract & Hidden Semantics (decode physical vs logical input, mutation rules, return type)
   - Worked Example by Hand (full trace table with state at every step)
   - Clarifying Questions

4. **Phase 2 — Approaches.** Write only:
   - Alternative Approaches & Tradeoffs (with counterexamples and missing proof insights)
   - Core Insight (1-3 sentences)

5. **Phase 3 — Proof.** Write only:
   - Formal State Model (variables, transitions, loop guard)
   - Correctness Proof with three separate claims:
     - Main invariant (initialization, maintenance, conclusion)
     - Safety claim (with algebra)
     - Termination (what decreases, upper bound, why remaining elements are correct)

6. **Phase 4 — Mapping.** Write only:
   - Equation → Pseudocode → Code Mapping (state variables, transitions, branch explanations, likely bug spots)

7. **Phase 5 — Supporting Sections.** Write:
   - Complexity Analysis (comparison table across approaches)
   - Edge Cases & Pitfalls
   - Transferable Pattern Recognition
   - Problem Variations & Follow-Ups (2-3 realistic ones)
   - Interview Questions (In-Problem Follow-Ups + Post-Solution Probes, 2-3 each)
   - Self-Test Questions (3-5)
   - Next Step Before Coding

8. **Generate Graphviz visuals.** Create `generate_visuals.py` that outputs `.png` to `png/` and `.dot` to `dot/`. Generate at least 4 diagrams with distinct teaching purposes: problem setup, rejected approach visualization, optimal state transitions, safety invariant, edge-case behavior.

9. **Assemble the README.** Merge all phases into the final `README.md` in section order with embedded diagram links.

10. **Commit and push.**
    ```bash
    cd ~/leetcode && git add . && git commit -m "Add {number}-{slug} study guide" && git push
    ```
