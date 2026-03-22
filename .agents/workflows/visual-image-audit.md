---
description: Formally audit every generated README image before signoff, commit, or push
---

# Audit Generated README Images

Run this workflow immediately after image generation and before:
- final README edits are treated as complete,
- structural audit is treated as meaningful,
- commits are created,
- or changes are pushed.

This audit does not stop at checking that files exist. Each image must be evaluated as a teaching artifact.

## Scope

Audit every image embedded from local `png/` assets in the README.

If the README embeds 18 images, audit 18 images.
Do not sample. Do not audit only the newest ones.

## Per-Image Audit Checklist

For each embedded image, verify all of the following:

### 1. Render Integrity
- The file exists locally under `png/`.
- The file is non-empty.
- The image renders without corruption.
- Text is legible at normal README viewing size.
- Labels are not clipped, overlapping, or truncated.

### 2. README Alignment
- The image filename matches the README embed.
- The surrounding intro sentences accurately describe what the image teaches.
- The follow-up interpretation accurately states why the image matters.
- The `alt` text is specific and matches the actual content.

### 3. Teaching Purpose
- The image has one clear teaching purpose.
- That purpose is distinct from neighboring visuals.
- The image removes a real confusion hotspot, not just repeats a prior diagram.
- If the image is decorative, redundant, or vague, it fails.

### 4. Mathematical / Algorithmic Correctness
- The image matches the algorithm described in the nearby text.
- Numeric examples shown in the image are correct.
- Pointer movements, pruned regions, invariants, and edge-case behavior are logically valid.
- If the image claims a proof step, the proof step must actually be sound.

### 5. Reproducibility
- The image is locally reproducible from repository assets.
- If the visual set is nontrivial, the generator and source files exist and match the embedded images.
- No core teaching image may rely on an external hotlink.

## Required Evaluation Output

Do the audit as a checklist or table in your working process, one row per image.

Minimum columns:
- `Image`
- `Purpose`
- `Pass/Fail`
- `Issues`
- `Fix`

If any image fails:
- fix the image, README text, generator, or source graph,
- regenerate the assets,
- and re-audit the full image set.

Do not mark the visual section complete until every embedded image passes.

## Whole-Set Failure Conditions

The visual set fails if any of the following is true:
- any embedded image is missing,
- any embedded image is empty,
- any embedded image is unreadable,
- any embedded image is mathematically wrong,
- any embedded image is redundant filler,
- any embedded image is externally hotlinked,
- or the README text around an image misstates what the image shows.

## Audit Mindset

Treat the image audit the same way you would treat a proof audit:
- visual clarity matters,
- correctness matters,
- and explanatory value matters.

Passing file-existence checks is not enough.
