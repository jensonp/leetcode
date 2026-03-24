#!/bin/bash
# Structural audit for a LeetCode README
# Usage: ./audit.sh 011-container-with-most-water

DIR="${1:?Usage: ./audit.sh <problem-dir>}"
README="$DIR/README.md"

if [ ! -f "$README" ]; then
  echo "❌ No README.md found in $DIR"
  exit 1
fi

TITLE_PATTERN='^# .+'

NEW_REQUIRED_HEADINGS=(
  "## Fundamentals"
  "### Problem Contract"
  "### Definitions and State Model"
  "### Key Lemma / Invariant / Recurrence"
  "### Algorithm"
  "### Correctness Proof"
  "### Complexity Analysis"
  "## Appendix"
  "### Visuals"
)

NEW_OPTIONAL_HEADINGS=(
  "### Correctness-Sensitive Pitfalls"
  "### Worked Example"
  "### Visuals"
  "### Variants / Follow-Ups"
  "### Common Pitfalls"
  "### Implementation Notes"
  "### Interview Explanation"
  "### Self-Test Questions"
  "### Why Naive / Wrong Approaches Fail"
  "### Final Code"
)

LEGACY_REQUIRED_HEADINGS=(
  "# Problem Metadata"
  "# Problem Contract & Hidden Semantics"
  "# Worked Example by Hand"
  "# Alternative Approaches & Tradeoffs"
  "# Core Insight"
  "# Formal State Model"
  "# Optimal Approach"
  "# Correctness Proof"
  "# Equation -> Pseudocode -> Implementation Mapping"
  "# Visualizing the Algorithm"
  "# Complexity Analysis"
  "# Edge Cases & Pitfalls"
  "# Problem Variations & Follow-Ups"
)

LEGACY_OPTIONAL_HEADINGS=(
  "# Conceptual Glossary"
  "# Clarifying Questions"
  "# What Breaks If"
  "# Transferable Pattern Recognition"
  "# Interview Questions"
  "# Interview Simulation Questions"
  "# Self-Test Questions"
  "# Next Step Before Coding"
)

echo "Auditing: $README"
echo "========================="

PASS=0
FAIL=0

if grep -qE "$TITLE_PATTERN" "$README"; then
  echo "  ✅ Top-level title found"
  PASS=$((PASS + 1))
else
  echo "  ❌ MISSING: top-level title"
  FAIL=$((FAIL + 1))
fi

if grep -qF "## Fundamentals" "$README"; then
  MODE="fundamentals_appendix"
  REQUIRED_HEADINGS=("${NEW_REQUIRED_HEADINGS[@]}")
  OPTIONAL_HEADINGS=("${NEW_OPTIONAL_HEADINGS[@]}")
  echo "  ✅ Layout detected: Fundamentals/Appendix"
  PASS=$((PASS + 1))
else
  MODE="legacy"
  REQUIRED_HEADINGS=("${LEGACY_REQUIRED_HEADINGS[@]}")
  OPTIONAL_HEADINGS=("${LEGACY_OPTIONAL_HEADINGS[@]}")
  echo "  ℹ️  Layout detected: legacy"
fi

for heading in "${REQUIRED_HEADINGS[@]}"; do
  if grep -qF "$heading" "$README"; then
    echo "  ✅ $heading"
    PASS=$((PASS + 1))
  else
    echo "  ❌ MISSING: $heading"
    FAIL=$((FAIL + 1))
  fi
done

for heading in "${OPTIONAL_HEADINGS[@]}"; do
  if grep -qF "$heading" "$README"; then
    echo "  ℹ️  Optional heading present: $heading"
  fi
done

PNG_COUNT=$(find "$DIR/png" -type f -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
NONEMPTY_PNG_COUNT=$(find "$DIR/png" -type f -name "*.png" -size +0c 2>/dev/null | wc -l | tr -d ' ')

EMBEDDED_PNGS=$(
  grep -oE 'src="png/[^"]+\.png"' "$README" \
    | sed -E 's/src="([^"]+)"/\1/' \
    | sort -u
)

if [ -n "$EMBEDDED_PNGS" ]; then
  EMBEDDED_COUNT=$(printf '%s\n' "$EMBEDDED_PNGS" | sed '/^$/d' | wc -l | tr -d ' ')
else
  EMBEDDED_COUNT=0
fi

if [ "$PNG_COUNT" -gt 0 ]; then
  echo "  ✅ Diagram files: $PNG_COUNT found"
  PASS=$((PASS + 1))
else
  echo "  ❌ Diagram files: required, none found"
  FAIL=$((FAIL + 1))
fi

if [ "$PNG_COUNT" -eq 0 ]; then
  echo "  ❌ Non-empty diagrams: no diagram set exists"
  FAIL=$((FAIL + 1))
elif [ "$NONEMPTY_PNG_COUNT" -gt 0 ]; then
  echo "  ✅ Non-empty diagrams: $NONEMPTY_PNG_COUNT found"
  PASS=$((PASS + 1))
else
  echo "  ❌ Non-empty diagrams: none found"
  FAIL=$((FAIL + 1))
fi

if [ "$EMBEDDED_COUNT" -gt 0 ]; then
  echo "  ✅ Embedded local PNGs: $EMBEDDED_COUNT found"
  PASS=$((PASS + 1))
else
  echo "  ❌ Embedded local PNGs: required, none found"
  FAIL=$((FAIL + 1))
fi

MISSING_OR_EMPTY=0
if [ -n "$EMBEDDED_PNGS" ]; then
  while IFS= read -r rel_path; do
    full_path="$DIR/$rel_path"
    if [ ! -f "$full_path" ] || [ ! -s "$full_path" ]; then
      echo "  ❌ Broken embedded image: $rel_path"
      MISSING_OR_EMPTY=$((MISSING_OR_EMPTY + 1))
    fi
  done <<EOF
$EMBEDDED_PNGS
EOF
fi

if [ "$MISSING_OR_EMPTY" -eq 0 ]; then
  echo "  ✅ Embedded image files exist and are non-empty"
  PASS=$((PASS + 1))
else
  FAIL=$((FAIL + MISSING_OR_EMPTY))
fi

EXTERNAL_IMG_COUNT=$(grep -oE '<img[^>]+src="https?://[^"]+"' "$README" 2>/dev/null | wc -l | tr -d ' ')
if [ "$EXTERNAL_IMG_COUNT" -eq 0 ]; then
  echo "  ✅ External image embeds: none"
  PASS=$((PASS + 1))
else
  echo "  ❌ External image embeds found: $EXTERNAL_IMG_COUNT"
  FAIL=$((FAIL + EXTERNAL_IMG_COUNT))
fi

RAW_LATEX_DISPLAY_COUNT=$(grep -oE '\\\[|\\\]' "$README" 2>/dev/null | wc -l | tr -d ' ')
if [ "$RAW_LATEX_DISPLAY_COUNT" -eq 0 ]; then
  echo "  ✅ Render-safe math delimiters: no raw \\\\[ \\\\] blocks"
  PASS=$((PASS + 1))
else
  echo "  ❌ Render-safe math delimiters: found $RAW_LATEX_DISPLAY_COUNT raw \\\\[ or \\\\] tokens"
  FAIL=$((FAIL + 1))
fi

if [ "$MODE" = "fundamentals_appendix" ]; then
  FUNDAMENTALS_TEXT=$(
    awk '
      /^## Fundamentals$/ { in_fundamentals=1; next }
      /^## Appendix$/ { in_fundamentals=0 }
      in_fundamentals { print }
    ' "$README"
  )

  WEAK_REFERENT_COUNT=$(
    printf '%s\n' "$FUNDAMENTALS_TEXT" \
      | grep -E -i 'the two chosen lines|the current pair|the shorter line|the two lines|lines at indices|volume' \
      | wc -l | tr -d ' '
  )

  if [ "$WEAK_REFERENT_COUNT" -eq 0 ]; then
    echo "  ✅ Referential clarity in Fundamentals: no banned weak phrases"
    PASS=$((PASS + 1))
  else
    echo "  ❌ Referential clarity in Fundamentals: found $WEAK_REFERENT_COUNT banned weak phrase match(es)"
    FAIL=$((FAIL + 1))
  fi
fi

echo "========================="
echo "Result: $PASS passed, $FAIL failed"

if [ "$FAIL" -eq 0 ]; then
  echo "✅ README passes structural audit."
else
  echo "❌ README has $FAIL issue(s)."
  exit 1
fi
