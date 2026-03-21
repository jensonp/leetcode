#!/bin/bash
# Quick structural audit of a LeetCode README
# Usage: ./audit.sh 088-merge-sorted-array

DIR="${1:?Usage: ./audit.sh <problem-dir>}"
README="$DIR/README.md"

if [ ! -f "$README" ]; then
  echo "❌ No README.md found in $DIR"
  exit 1
fi

REQUIRED_HEADINGS=(
  "# Problem Metadata"
  "# Problem Contract & Hidden Semantics"
  "# Worked Example by Hand"
  "# Clarifying Questions"
  "# Alternative Approaches & Tradeoffs"
  "# Core Insight"
  "# Formal State Model"
  "# Optimal Approach"
  "# Correctness Proof"
  "# Complexity Analysis"
  "# What Breaks If"
  "# Edge Cases & Pitfalls"
  "# Transferable Pattern Recognition"
  "# Problem Variations & Follow-Ups"
  "# Interview Questions"
  "# Self-Test Questions"
  "# Next Step Before Coding"
)

echo "Auditing: $README"
echo "========================="

PASS=0
FAIL=0

for heading in "${REQUIRED_HEADINGS[@]}"; do
  if grep -qF "$heading" "$README"; then
    echo "  ✅ $heading"
    PASS=$((PASS + 1))
  else
    echo "  ❌ MISSING: $heading"
    FAIL=$((FAIL + 1))
  fi
done

# Check for diagrams
PNG_COUNT=$(find "$DIR/png" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
if [ "$PNG_COUNT" -ge 10 ]; then
  echo "  ✅ Diagrams: $PNG_COUNT found (≥10 required)"
  PASS=$((PASS + 1))
else
  echo "  ❌ Diagrams: only $PNG_COUNT found (≥10 required)"
  FAIL=$((FAIL + 1))
fi

echo "========================="
echo "Result: $PASS passed, $FAIL failed"

if [ "$FAIL" -eq 0 ]; then
  echo "✅ README passes structural audit."
else
  echo "❌ README has $FAIL issue(s)."
  exit 1
fi
