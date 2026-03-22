#!/usr/bin/env python3

from __future__ import annotations

import html
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOT_DIR = ROOT / "dot"
PNG_DIR = ROOT / "png"
HEIGHTS = [1, 8, 6, 2, 5, 4, 8, 3, 7]
N = len(HEIGHTS)

HEADER_BG = "#E2E8F0"
BLANK_BG = "#F8FAFC"
LEFT_BG = "#BFDBFE"
RIGHT_BG = "#FCD34D"
SUCCESS_BG = "#BBF7D0"
BEST_BG = "#FDE68A"
PATH_BG = "#C7D2FE"
PRUNED_BG = "#E5E7EB"
MUTED_TEXT = "#475569"
TEXT = "#0F172A"
ACCENT_BG = "#FCE7F3"


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def quote(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def font(text: object, *, size: int = 12, color: str = TEXT, bold: bool = False) -> str:
    content = esc(text).replace("\n", "<BR/>")
    if not content:
        content = " "
    if bold:
        content = f"<B>{content}</B>"
    return f'<FONT POINT-SIZE="{size}" COLOR="{color}">{content}</FONT>'


def td(
    text: object = "",
    *,
    bg: str = "#FFFFFF",
    color: str = TEXT,
    colspan: int = 1,
    bold: bool = False,
    size: int = 12,
) -> str:
    attrs = [
        f'BGCOLOR="{bg}"',
        'BORDER="1"',
        'COLOR="#CBD5E1"',
        'CELLPADDING="8"',
    ]
    if colspan != 1:
        attrs.append(f'COLSPAN="{colspan}"')
    return f'<TD {" ".join(attrs)}>{font(text, size=size, color=color, bold=bold)}</TD>'


def table(rows: list[list[str]]) -> str:
    rendered_rows = "".join(f"<TR>{''.join(row)}</TR>" for row in rows)
    return (
        '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">'
        f"{rendered_rows}</TABLE>"
    )


def note_node(name: str, title: str, lines: list[str], *, fill: str = "#FFFFFF") -> str:
    label = "\n".join([title, *lines])
    return (
        f'{name} [shape=box style="rounded,filled" fillcolor="{fill}" '
        f'color="#94A3B8" penwidth=1.2 margin="0.18,0.12" '
        f'label="{quote(label)}"];'
    )


def area(i: int, j: int) -> int:
    return (j - i) * min(HEIGHTS[i], HEIGHTS[j])


def array_node(
    name: str,
    title: str,
    *,
    left: int | None = None,
    right: int | None = None,
    faded: set[int] | None = None,
    custom_bg: dict[int, str] | None = None,
    custom_role: dict[int, str] | None = None,
) -> str:
    faded = faded or set()
    custom_bg = custom_bg or {}
    custom_role = custom_role or {}

    def cell_bg(idx: int) -> str:
        if idx in custom_bg:
            return custom_bg[idx]
        if idx in faded:
            return PRUNED_BG
        if idx == left:
            return LEFT_BG
        if idx == right:
            return RIGHT_BG
        return "#FFFFFF"

    def role(idx: int) -> str:
        if idx in custom_role:
            return custom_role[idx]
        labels: list[str] = []
        if idx == left:
            labels.append("left")
        if idx == right:
            labels.append("right")
        if left is not None and right is not None and left < idx < right:
            labels.append("inner")
        return " / ".join(labels)

    rows = [
        [td(title, bg=HEADER_BG, bold=True, colspan=N + 1)],
        [td("index", bg=HEADER_BG, bold=True)]
        + [td(idx, bg=cell_bg(idx), bold=idx in {left, right}) for idx in range(N)],
        [td("height", bg=HEADER_BG, bold=True)]
        + [td(value, bg=cell_bg(idx), bold=idx in {left, right}) for idx, value in enumerate(HEIGHTS)],
        [td("role", bg=HEADER_BG, bold=True)]
        + [
            td(
                role(idx),
                bg=cell_bg(idx),
                size=10,
                color=MUTED_TEXT if idx not in {left, right} else TEXT,
            )
            for idx in range(N)
        ],
    ]
    return f"{name} [shape=plain label=<{table(rows)}>];"


def custom_array_node(
    name: str,
    title: str,
    values: list[int],
    *,
    left: int | None = None,
    right: int | None = None,
    custom_role: dict[int, str] | None = None,
    custom_bg: dict[int, str] | None = None,
) -> str:
    custom_role = custom_role or {}
    custom_bg = custom_bg or {}
    local_n = len(values)

    def bg(idx: int) -> str:
        if idx in custom_bg:
            return custom_bg[idx]
        if idx == left:
            return LEFT_BG
        if idx == right:
            return RIGHT_BG
        return "#FFFFFF"

    def role(idx: int) -> str:
        if idx in custom_role:
            return custom_role[idx]
        labels: list[str] = []
        if idx == left:
            labels.append("left")
        if idx == right:
            labels.append("right")
        if left is not None and right is not None and left < idx < right:
            labels.append("inner")
        return " / ".join(labels)

    rows = [
        [td(title, bg=HEADER_BG, bold=True, colspan=local_n + 1)],
        [td("index", bg=HEADER_BG, bold=True)]
        + [td(idx, bg=bg(idx), bold=idx in {left, right}) for idx in range(local_n)],
        [td("height", bg=HEADER_BG, bold=True)]
        + [td(value, bg=bg(idx), bold=idx in {left, right}) for idx, value in enumerate(values)],
        [td("role", bg=HEADER_BG, bold=True)]
        + [td(role(idx), bg=bg(idx), size=10, color=MUTED_TEXT) for idx in range(local_n)],
    ]
    return f"{name} [shape=plain label=<{table(rows)}>];"


def matrix_node(
    name: str,
    title: str,
    *,
    current: tuple[int, int] | None = None,
    best: tuple[int, int] | None = None,
    pruned_rows: set[int] | None = None,
    pruned_cols: set[int] | None = None,
    path_numbers: dict[tuple[int, int], int] | None = None,
) -> str:
    pruned_rows = pruned_rows or set()
    pruned_cols = pruned_cols or set()
    path_numbers = path_numbers or {}

    rows: list[list[str]] = [
        [td(title, bg=HEADER_BG, bold=True, colspan=N + 1)],
        [td("i \\ j", bg=HEADER_BG, bold=True)]
        + [td(j, bg=HEADER_BG, bold=True) for j in range(N)],
    ]

    for i in range(N):
        row = [td(i, bg=HEADER_BG, bold=True)]
        for j in range(N):
            if j <= i:
                row.append(td("", bg=BLANK_BG))
                continue

            bg = "#FFFFFF"
            color = TEXT
            label = f"({i},{j})\nA={area(i, j)}"

            if i in pruned_rows or j in pruned_cols:
                bg = PRUNED_BG
                color = MUTED_TEXT
            if (i, j) in path_numbers:
                bg = PATH_BG
                label = f"step {path_numbers[(i, j)]}\n({i},{j})"
            if best == (i, j):
                bg = BEST_BG
                label = f"best\n({i},{j})\nA={area(i, j)}"
                color = TEXT
            if current == (i, j):
                bg = SUCCESS_BG
                label = f"current\n({i},{j})\nA={area(i, j)}"
                color = TEXT

            row.append(td(label, bg=bg, color=color, size=10))
        rows.append(row)

    return f"{name} [shape=plain label=<{table(rows)}>];"


def wrap_graph(body: str, *, rankdir: str = "LR") -> str:
    return f"""digraph G {{
graph [rankdir={rankdir} bgcolor="white" margin=0.18 pad=0.2 nodesep=0.45 ranksep=0.5 splines=line]
node [fontname="Helvetica" fontsize=12 color="#94A3B8"]
edge [fontname="Helvetica" fontsize=11 color="#64748B" arrowsize=0.7]
{body}
}}
"""


def visual_1() -> str:
    body = "\n".join(
        [
            array_node("arr", "Sample array: choose boundaries at indices 1 and 8", left=1, right=8),
            note_node(
                "stats",
                "Container math",
                ["width = 8 - 1 = 7", "water level = min(8, 7) = 7", "area = 49"],
                fill="#ECFCCB",
            ),
            note_node(
                "lesson",
                "Teaching point",
                ["Only the chosen endpoints matter.", "Inner lines do not displace water."],
                fill="#F8FAFC",
            ),
            "arr -> stats [style=dashed];",
            "stats -> lesson [style=dashed];",
            "{ rank=same; arr; stats; lesson; }",
        ]
    )
    return wrap_graph(body)


def visual_2() -> str:
    body = "\n".join(
        [
            matrix_node("pairs", "Every upper-triangular cell is one candidate pair"),
            note_node(
                "count",
                "Search space size",
                ["For n = 9 there are 9 * 8 / 2 = 36 pairs.", "Brute force touches every valid cell."],
                fill="#F8FAFC",
            ),
            "pairs -> count [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_3() -> str:
    body = "\n".join(
        [
            array_node(
                "arr",
                "Step 1: start with the widest possible pair (0, 8)",
                left=0,
                right=8,
                custom_role={0: "left / shorter", 8: "right / taller"},
            ),
            note_node(
                "eval",
                "Evaluate",
                ["width = 8", "water level = 1", "area = 8"],
                fill="#F8FAFC",
            ),
            note_node(
                "move",
                "Decision",
                ["height[0] = 1 is the bottleneck.", "Move left inward."],
                fill="#DBEAFE",
            ),
            "arr -> eval [style=dashed];",
            "eval -> move [label=\"shorter side decides\"];",
            "{ rank=same; arr; eval; move; }",
        ]
    )
    return wrap_graph(body)


def visual_4() -> str:
    body = "\n".join(
        [
            matrix_node(
                "prune",
                "After evaluating (0, 8), discard every pair anchored at i = 0",
                current=(0, 8),
                pruned_rows={0},
            ),
            note_node(
                "proof",
                "Why row 0 is safe to prune",
                ["Every (0, k) is narrower than (0, 8).", "Its water level is still capped at 1."],
                fill="#FEE2E2",
            ),
            "prune -> proof [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_5() -> str:
    body = "\n".join(
        [
            array_node(
                "arr",
                "Step 2: pair (1, 8) becomes the best container in the example",
                left=1,
                right=8,
                custom_bg={6: ACCENT_BG},
                custom_role={6: "inner tall line"},
            ),
            note_node(
                "best",
                "Best so far",
                ["width = 7", "water level = 7", "max_area = 49"],
                fill="#FEF3C7",
            ),
            note_node(
                "insight",
                "Teaching point",
                ["The line at index 6 is also tall.", "It still loses because the width is smaller."],
                fill="#F8FAFC",
            ),
            "arr -> best [style=dashed];",
            "best -> insight [style=dashed];",
            "{ rank=same; arr; best; insight; }",
        ]
    )
    return wrap_graph(body)


def visual_6() -> str:
    body = "\n".join(
        [
            matrix_node(
                "prune",
                "At pair (1, 8), the shorter right wall lets us prune column j = 8",
                current=(1, 8),
                best=(1, 8),
                pruned_cols={8},
            ),
            note_node(
                "proof",
                "Symmetric pruning",
                ["Every (k, 8) with k > 1 is narrower than (1, 8).", "Its water level cannot exceed 7."],
                fill="#FEE2E2",
            ),
            "prune -> proof [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_7() -> str:
    body = "\n".join(
        [
            array_node("arr", "Tie case: indices 1 and 6 both have height 8", left=1, right=6),
            note_node(
                "tie",
                "Equal heights",
                ["area = (6 - 1) * 8 = 40", "Either pointer may move safely."],
                fill="#EDE9FE",
            ),
            note_node("left", "Option A", ["Move left to 2"], fill="#DBEAFE"),
            note_node("right", "Option B", ["Move right to 5"], fill="#FDE68A"),
            "arr -> tie [style=dashed];",
            "tie -> left [label=\"safe\"];",
            "tie -> right [label=\"safe\"];",
            "{ rank=same; arr; tie; left; right; }",
        ]
    )
    return wrap_graph(body)


def visual_8() -> str:
    path = {
        (0, 8): 1,
        (1, 8): 2,
        (1, 7): 3,
        (1, 6): 4,
        (1, 5): 5,
        (1, 4): 6,
        (1, 3): 7,
        (1, 2): 8,
    }
    body = "\n".join(
        [
            matrix_node(
                "path",
                "The two-pointer algorithm walks a single O(n) path through the matrix",
                path_numbers=path,
                best=(1, 8),
            ),
            note_node(
                "count",
                "Why this is linear",
                ["Each step moves exactly one pointer inward.", "The path length is at most n - 1."],
                fill="#DBEAFE",
            ),
            "path -> count [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_9() -> str:
    body = "\n".join(
        [
            matrix_node(
                "inv",
                "Invariant view: pruned cells are gone, but the answer is not lost",
                best=(1, 8),
                current=(1, 7),
                pruned_rows={0},
                pruned_cols={8},
            ),
            note_node(
                "claim",
                "Main invariant",
                [
                    "Either the optimum has already been recorded.",
                    "Or it lies inside the current pointer window.",
                ],
                fill="#ECFCCB",
            ),
            "inv -> claim [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_10() -> str:
    body = "\n".join(
        [
            array_node("start", "Current pair", left=0, right=8, custom_role={0: "shorter", 8: "taller"}),
            note_node("start_note", "Area now", ["(8 - 0) * min(1, 7) = 8"], fill="#F8FAFC"),
            array_node("wrong", "Wrong move: keep the short wall, move the taller wall", left=0, right=7),
            note_node("wrong_note", "Result", ["(7 - 0) * min(1, 3) = 7", "Width shrinks, bottleneck stays 1."], fill="#FEE2E2"),
            array_node("right_move", "Correct move: discard the short wall", left=1, right=8),
            note_node("right_note", "Result", ["(8 - 1) * min(8, 7) = 49", "This is the global maximum."], fill="#ECFCCB"),
            "start -> start_note [style=dashed];",
            "start_note -> wrong [label=\"move taller\", color=\"#DC2626\", fontcolor=\"#DC2626\"];",
            "start_note -> right_move [label=\"move shorter\", color=\"#059669\", fontcolor=\"#059669\"];",
            "wrong -> wrong_note [style=dashed color=\"#DC2626\"];",
            "right_move -> right_note [style=dashed color=\"#059669\"];",
        ]
    )
    return wrap_graph(body, rankdir="TB")


def visual_11() -> str:
    body = "\n".join(
        [
            'decide [shape=box style="rounded,filled" fillcolor="#F8FAFC" label="Compare\\nheight[left] and height[right]"];',
            'less [shape=box style="rounded,filled" fillcolor="#DBEAFE" label="height[left] < height[right]\\nMove left"];',
            'greater [shape=box style="rounded,filled" fillcolor="#FDE68A" label="height[left] > height[right]\\nMove right"];',
            'equal [shape=box style="rounded,filled" fillcolor="#EDE9FE" label="height[left] == height[right]\\nEither move is safe"];',
            'decide -> less [label="<"];',
            'decide -> greater [label=">"];',
            'decide -> equal [label="="];',
        ]
    )
    return wrap_graph(body, rankdir="TB")


def visual_12() -> str:
    body = "\n".join(
        [
            custom_array_node(
                "small",
                "Edge case: with two lines, there is only one possible container",
                [1, 1],
                left=0,
                right=1,
            ),
            note_node(
                "result",
                "What happens",
                ["Compute area once: (1 - 0) * min(1, 1) = 1", "Move one pointer and stop."],
                fill="#ECFCCB",
            ),
            "small -> result [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_13() -> str:
    body = "\n".join(
        [
            custom_array_node(
                "zeros",
                "Edge case: a zero-height wall makes the current container hold zero water",
                [0, 4, 0, 3],
                left=0,
                right=3,
                custom_role={0: "left / bottleneck", 3: "right"},
            ),
            note_node(
                "result",
                "Teaching point",
                ["width = 3, but min(0, 3) = 0", "Large width alone cannot rescue a zero bottleneck."],
                fill="#FEE2E2",
            ),
            "zeros -> result [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_14() -> str:
    body = "\n".join(
        [
            note_node("s1", "Step 2", ["pair (1, 8)", "area = 49"], fill="#ECFCCB"),
            note_node("s2", "Step 3", ["pair (1, 7)", "area = 18"], fill="#DBEAFE"),
            note_node("s3", "Step 4", ["pair (1, 6)", "area = 40"], fill="#FDE68A"),
            note_node("s4", "Step 5", ["pair (1, 5)", "area = 16"], fill="#DBEAFE"),
            's1 -> s2 [label="right wall shorter: 7 < 8"];',
            's2 -> s3 [label="right wall shorter: 3 < 8"];',
            's3 -> s4 [label="tie at 8 and 8: move either"];',
        ]
    )
    return wrap_graph(body)


def visual_15() -> str:
    rows = [
        [td("Approach", bg=HEADER_BG, bold=True), td("States touched on the sample", bg=HEADER_BG, bold=True), td("Why", bg=HEADER_BG, bold=True)],
        [td("Brute force"), td("36 pairs"), td("Checks every valid (i, j) combination")],
        [td("Two pointers", bg=SUCCESS_BG), td("8 pairs", bg=SUCCESS_BG), td("Prunes one full row or column every step", bg=SUCCESS_BG)],
    ]
    body = "\n".join(
        [
            f'compare [shape=plain label=<{table(rows)}>];',
            note_node(
                "lesson",
                "Why the optimization matters",
                ["The algorithm does not search less carefully.", "It discards provably inferior regions."],
                fill="#F8FAFC",
            ),
            "compare -> lesson [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_16() -> str:
    body = "\n".join(
        [
            array_node(
                "wide",
                "Best pair: (1, 8) uses slightly lower water level but much more width",
                left=1,
                right=8,
                custom_bg={6: ACCENT_BG},
            ),
            note_node(
                "wide_stats",
                "Area of (1, 8)",
                ["width = 7", "water level = 7", "area = 49"],
                fill="#ECFCCB",
            ),
            array_node(
                "narrow",
                "Inner tall line: (1, 6) is taller but too narrow to win",
                left=1,
                right=6,
                custom_bg={8: ACCENT_BG},
                custom_role={8: "previous wider partner"},
            ),
            note_node(
                "narrow_stats",
                "Area of (1, 6)",
                ["width = 5", "water level = 8", "area = 40"],
                fill="#FEE2E2",
            ),
            "wide -> wide_stats [style=dashed];",
            "narrow -> narrow_stats [style=dashed];",
            "{ rank=same; wide; wide_stats; narrow; narrow_stats; }",
        ]
    )
    return wrap_graph(body)


def visual_17() -> str:
    body = "\n".join(
        [
            matrix_node(
                "tie_prune",
                "Tie optimization: at (1, 6), both the active row and column are safe to drop",
                current=(1, 6),
                best=(1, 8),
                pruned_rows={1},
                pruned_cols={6},
            ),
            note_node(
                "proof",
                "Why moving both is safe",
                [
                    "Inside the active window, every (1, k) and (k, 6) is narrower.",
                    "Their water level cannot exceed 8.",
                ],
                fill="#EDE9FE",
            ),
            "tie_prune -> proof [style=dashed];",
        ]
    )
    return wrap_graph(body)


def visual_18() -> str:
    body = "\n".join(
        [
            note_node("s1", "(0, 8)", ["width = 8"], fill="#DBEAFE"),
            note_node("s2", "(1, 8)", ["width = 7"], fill="#ECFCCB"),
            note_node("s3", "(1, 7)", ["width = 6"], fill="#DBEAFE"),
            note_node("s4", "(1, 6)", ["width = 5"], fill="#DBEAFE"),
            note_node("s5", "(1, 5)", ["width = 4"], fill="#DBEAFE"),
            note_node("s6", "(1, 4)", ["width = 3"], fill="#DBEAFE"),
            note_node("s7", "(1, 3)", ["width = 2"], fill="#DBEAFE"),
            note_node("s8", "(1, 2)", ["width = 1"], fill="#DBEAFE"),
            note_node("done", "Stop", ["Pointers meet at (1, 1)", "No width remains."], fill="#FEE2E2"),
            's1 -> s2 [label="move left"];',
            's2 -> s3 [label="move right"];',
            's3 -> s4 [label="move right"];',
            's4 -> s5 [label="move either"];',
            's5 -> s6 [label="move right"];',
            's6 -> s7 [label="move right"];',
            's7 -> s8 [label="move right"];',
            's8 -> done [label="move right"];',
        ]
    )
    return wrap_graph(body)


def render_visual(name: str, dot_source: str) -> None:
    dot_path = DOT_DIR / f"{name}.dot"
    png_path = PNG_DIR / f"{name}.png"
    dot_path.write_text(dot_source, encoding="utf-8")
    subprocess.run(["dot", "-Tpng", str(dot_path), "-o", str(png_path)], check=True)


def main() -> None:
    DOT_DIR.mkdir(exist_ok=True)
    PNG_DIR.mkdir(exist_ok=True)

    visuals = {
        "visual_1": visual_1(),
        "visual_2": visual_2(),
        "visual_3": visual_3(),
        "visual_4": visual_4(),
        "visual_5": visual_5(),
        "visual_6": visual_6(),
        "visual_7": visual_7(),
        "visual_8": visual_8(),
        "visual_9": visual_9(),
        "visual_10": visual_10(),
        "visual_11": visual_11(),
        "visual_12": visual_12(),
        "visual_13": visual_13(),
        "visual_14": visual_14(),
        "visual_15": visual_15(),
        "visual_16": visual_16(),
        "visual_17": visual_17(),
        "visual_18": visual_18(),
    }

    for name, dot_source in visuals.items():
        render_visual(name, dot_source)
        print(f"rendered {name}")


if __name__ == "__main__":
    main()
