#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import subprocess
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent

TARGETS = [
    "003-longest-substring-without-repeating-characters",
    "004-median-of-two-sorted-arrays",
    "015-3sum",
    "025-reverse-nodes-in-k-group",
    "033-search-in-rotated-sorted-array",
    "039-combination-sum",
    "042-trapping-rain-water",
    "045-jump-game-ii",
    "051-n-queens",
    "055-jump-game",
    "056-merge-intervals",
    "057-insert-interval",
    "071-simplify-path",
    "072-edit-distance",
    "073-set-matrix-zeroes",
    "076-minimum-window-substring",
    "079-word-search",
    "097-interleaving-string",
    "098-validate-binary-search-tree",
    "105-construct-binary-tree-from-preorder-and-inorder-traversal",
    "114-flatten-binary-tree-to-linked-list",
    "123-best-time-to-buy-and-sell-stock-iii",
    "124-binary-tree-maximum-path-sum",
    "127-word-ladder",
    "128-longest-consecutive-sequence",
    "130-surrounded-regions",
    "133-clone-graph",
    "134-gas-station",
    "135-candy",
    "138-copy-list-with-random-pointer",
    "139-word-break",
    "146-lru-cache",
    "188-best-time-to-buy-and-sell-stock-iv",
    "198-house-robber",
    "200-number-of-islands",
    "207-course-schedule",
    "208-implement-trie-prefix-tree",
    "212-word-search-ii",
    "224-basic-calculator",
    "236-lowest-common-ancestor-of-a-binary-tree",
    "238-product-of-array-except-self",
    "295-find-median-from-data-stream",
    "300-longest-increasing-subsequence",
    "322-coin-change",
    "452-minimum-number-of-arrows-to-burst-balloons",
]

HEADER_BG = "#E2E8F0"
STATE_BG = "#DBEAFE"
CLAIM_BG = "#DCFCE7"
ACTION_BG = "#FDE68A"
PROOF_BG = "#FCE7F3"
MUTED_BG = "#F8FAFC"
TEXT = "#0F172A"
MUTED = "#475569"
EDGE = "#64748B"
BORDER = "#94A3B8"


CUSTOM_VISUALS = {
    "042-trapping-rain-water": {
        "title": "Finalizing One Side When `left_max <= right_max`",
        "alt": "Bar chart style view showing why the left index can be finalized when left_max is smaller",
        "followup": "This picture makes the proof move concrete: once the smaller boundary is the left side, the water above that index is already determined and can be added permanently.",
    },
    "025-reverse-nodes-in-k-group": {
        "title": "Reverse One k-Block, Then Splice It Back",
        "alt": "Linked-list diagram showing group_prev, kth, group_next, and the reversed segment",
        "followup": "The purpose is to lock in the segment boundaries before rewiring, then show exactly how the reversed block reconnects to the untouched suffix.",
    },
    "073-set-matrix-zeroes": {
        "title": "First Row And First Column As Marker Storage",
        "alt": "Matrix snapshot showing interior zeros writing row and column markers into the first row and first column",
        "followup": "This is the one picture worth keeping in mind: the first pass writes metadata into the matrix itself, and `matrix[0][0]` is not enough to represent both border directions alone.",
    },
    "004-median-of-two-sorted-arrays": {
        "title": "Binary Search On The Partition Boundary",
        "alt": "Two sorted arrays with cut positions i and j and the four boundary values Aleft, Aright, Bleft, Bright",
        "followup": "The cut positions, not the raw arrays, are the real state. The visual shows exactly which four values decide whether the partition is feasible and which direction the search must move.",
    },
    "114-flatten-binary-tree-to-linked-list": {
        "title": "Reverse Preorder Builds The Correct Suffix",
        "alt": "Tree sketch and right-skewed list showing why processing right then left makes prev the correct suffix",
        "followup": "The reverse-preorder order is the non-obvious part. This sketch shows that `prev` already represents the list suffix that should follow the current node.",
    },
    "146-lru-cache": {
        "title": "Hash Map + Recency List Representation",
        "alt": "Diagram of a hash map pointing into a doubly linked list ordered from most recent to least recent",
        "followup": "This is the representation invariant the whole design depends on: the map gives constant-time access to nodes, and the list gives constant-time promotion and eviction.",
    },
    "212-word-search-ii": {
        "title": "Trie Prefixes Prune The Board Search",
        "alt": "Board path and trie path diagram showing successful prefix advance and a missing-child prune",
        "followup": "The image focuses on the real optimization: DFS continues only while the current board path is also a trie prefix, and a missing child kills the whole branch immediately.",
    },
}


def quote(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def wrap_lines(text: str, width: int = 30, max_lines: int = 5) -> list[str]:
    compact = " ".join(text.split())
    if not compact:
        return [" "]
    lines = textwrap.wrap(compact, width=width)
    if len(lines) > max_lines:
        lines = lines[: max_lines - 1] + ["..."]
    return lines


def note_node(name: str, title: str, lines: list[str], fill: str) -> str:
    label = "\n".join([title, *lines])
    return (
        f'{name} [shape=box style="rounded,filled" fillcolor="{fill}" '
        f'color="{BORDER}" penwidth=1.2 margin="0.18,0.12" '
        f'fontname="Helvetica" fontsize=12 label="{quote(label)}"];'
    )


def plain_node(name: str, text: str) -> str:
    return f'{name} [shape=plaintext fontname="Helvetica-Bold" fontsize=15 label="{quote(text)}"];'


def wrap_graph(body: str, title: str, rankdir: str = "LR") -> str:
    return f"""digraph G {{
graph [rankdir={rankdir} bgcolor="white" margin=0.18 pad=0.24 nodesep=0.55 ranksep=0.6 labelloc="t" label="{quote(title)}" fontsize=18 fontname="Helvetica-Bold"]
node [fontname="Helvetica" fontsize=12 color="{BORDER}"]
edge [fontname="Helvetica" fontsize=11 color="{EDGE}" arrowsize=0.7]
{body}
}}
"""


def first_section(text: str, heading: str) -> str:
    pattern = rf"^### {re.escape(heading)}\n(.*?)(?=^### |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    return match.group(1).strip() if match else ""


def strip_code_fences(section: str) -> str:
    lines = []
    in_fence = False
    for line in section.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        lines.append(line)
    return "\n".join(lines)


def first_paragraph(section: str) -> str:
    cleaned = strip_code_fences(section)
    blocks = [block.strip() for block in cleaned.split("\n\n") if block.strip()]
    for block in blocks:
        if block.startswith("#### "):
            continue
        return block
    return blocks[0] if blocks else ""


def first_subheading_and_paragraph(section: str) -> tuple[str, str]:
    lines = section.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith("#### "):
            title = line[5:].strip()
            paragraph_lines: list[str] = []
            for later in lines[idx + 1 :]:
                if later.startswith("#### "):
                    break
                if later.startswith("```"):
                    break
                paragraph_lines.append(later)
            paragraph = " ".join(part.strip() for part in paragraph_lines if part.strip())
            return title, paragraph
    return "Key Claim", first_paragraph(section)


def algorithm_summary(section: str) -> str:
    lines = []
    for line in strip_code_fences(section).splitlines():
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith("1. ") or stripped.startswith("- "):
            lines.append(stripped[3:] if stripped.startswith("1. ") else stripped[2:])
        elif not stripped.startswith("```"):
            lines.append(stripped)
        if len(lines) >= 3:
            break
    return " ".join(lines) if lines else first_paragraph(section)


def proof_summary(section: str) -> str:
    paragraph = first_paragraph(section)
    sentence = re.split(r"(?<=[.!?])\s+", paragraph.strip())[0]
    return sentence or paragraph


def read_title(readme_text: str) -> str:
    first_line = readme_text.splitlines()[0]
    return first_line.lstrip("# ").strip()


def generic_graph(problem_dir: str, readme_text: str) -> str:
    title = read_title(readme_text)
    defs = first_paragraph(first_section(readme_text, "Definitions and State Model"))
    claim_title, claim_text = first_subheading_and_paragraph(first_section(readme_text, "Key Lemma / Invariant / Recurrence"))
    algo = algorithm_summary(first_section(readme_text, "Algorithm"))
    proof = proof_summary(first_section(readme_text, "Correctness Proof"))

    body = "\n".join(
        [
            plain_node("top", title),
            note_node("state", "State Model", wrap_lines(defs), STATE_BG),
            note_node("claim", claim_title, wrap_lines(claim_text), CLAIM_BG),
            note_node("action", "Algorithm Consequence", wrap_lines(algo), ACTION_BG),
            note_node("proof", "Why It Works", wrap_lines(proof), PROOF_BG),
            "top -> state [style=invis];",
            "state -> claim [label=\"sets up\"];",
            "claim -> action [label=\"justifies\"];",
            "action -> proof [label=\"preserves\"];",
            "{ rank=same; state; claim; action; proof }",
        ]
    )
    return wrap_graph(body, f"{title}: core proof map")


def custom_array_table(
    title: str,
    headers: list[str],
    rows: list[list[str]],
    highlights: dict[tuple[int, int], str] | None = None,
) -> str:
    highlights = highlights or {}
    rendered_rows = []
    for r, row in enumerate(rows):
        cells = []
        for c, value in enumerate(row):
            bg = highlights.get((r, c), "#FFFFFF")
            color = TEXT if bg != MUTED_BG else MUTED
            display = esc(value) or " "
            cells.append(
                f'<TD BGCOLOR="{bg}" BORDER="1" COLOR="#CBD5E1" CELLPADDING="8"><FONT COLOR="{color}" POINT-SIZE="11">{display}</FONT></TD>'
            )
        rendered_rows.append(f"<TR>{''.join(cells)}</TR>")
    header_cells = "".join(
        f'<TD BGCOLOR="{HEADER_BG}" BORDER="1" COLOR="#CBD5E1" CELLPADDING="8"><B><FONT POINT-SIZE="11">{esc(h) or " "}</FONT></B></TD>'
        for h in headers
    )
    table = (
        '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">'
        f'<TR><TD BGCOLOR="{HEADER_BG}" BORDER="1" COLOR="#CBD5E1" COLSPAN="{len(headers)}" CELLPADDING="10"><B><FONT POINT-SIZE="13">{esc(title)}</FONT></B></TD></TR>'
        f"<TR>{header_cells}</TR>"
        f"{''.join(rendered_rows)}</TABLE>"
    )
    return table


def trapping_rain_graph() -> str:
    headers = ["i", "0", "1", "2", "3", "4", "5", "6", "7"]
    rows = [
        ["height", "0", "1", "0", "2", "1", "0", "1", "3"],
        ["role", "", "", "", "left_max=2", "l", "", "", "right_max=3"],
    ]
    highlights = {
        (0, 4): ACTION_BG,
        (0, 7): CLAIM_BG,
        (1, 4): ACTION_BG,
        (1, 3): STATE_BG,
        (1, 7): CLAIM_BG,
    }
    table = custom_array_table("Current window", headers, rows, highlights)
    body = "\n".join(
        [
            f"window [shape=plain label=<{table}>];",
            note_node("fact", "Finalization step", ["left_max = 2 <= right_max = 3", "water(4) = 2 - 1 = 1", "index 4 can be finalized now"], CLAIM_BG),
            note_node("move", "Pointer consequence", ["add 1 to the answer", "increment l", "future right choices cannot reduce the bound"], ACTION_BG),
            "window -> fact [label=\"read state\"];",
            "fact -> move [label=\"justifies move\"];",
        ]
    )
    return wrap_graph(body, "42: finalize the side with the smaller max")


def reverse_k_group_graph() -> str:
    before = 'before [shape=record style="filled" fillcolor="#DBEAFE" label="dummy | group_prev | a | b | c=kth | d=group_next | e"];'
    after = 'after [shape=record style="filled" fillcolor="#DCFCE7" label="dummy | group_prev | c | b | a | d=group_next | e"];'
    body = "\n".join(
        [
            before,
            after,
            note_node("segment", "Reverse block", ["preserve group_next = d", "reverse [a, b, c]", "splice c..a after group_prev"], ACTION_BG),
            'before -> segment [label="fix boundaries"];',
            'segment -> after [label="rewire once"];',
        ]
    )
    return wrap_graph(body, "25: reverse one k-block, then reconnect it")


def set_matrix_zeroes_graph() -> str:
    headers = ["", "0", "1", "2", "3"]
    rows = [
        ["0", "1", "0", "1", "1"],
        ["1", "0", "1", "1", "1"],
        ["2", "1", "1", "1", "0"],
        ["3", "1", "1", "1", "1"],
    ]
    highlights = {
        (0, 2): ACTION_BG,
        (1, 0): CLAIM_BG,
        (0, 1): CLAIM_BG,
        (2, 3): ACTION_BG,
        (2, 0): CLAIM_BG,
        (0, 3): CLAIM_BG,
    }
    table = custom_array_table("Interior zeros write row / column markers", headers, rows, highlights)
    body = "\n".join(
        [
            f"matrix [shape=plain label=<{table}>];",
            note_node("corner", "Special case", ["matrix[0][0] cannot encode", "both the first row and", "the first column alone"], PROOF_BG),
            note_node("flags", "Saved separately", ["first_row_zero", "first_col_zero"], STATE_BG),
            "matrix -> corner [label=\"why booleans exist\"];",
            "corner -> flags [label=\"store border metadata\"];",
        ]
    )
    return wrap_graph(body, "73: reuse the matrix itself as marker storage")


def median_partition_graph() -> str:
    a_headers = ["A", "0", "1", "2", "3", "4"]
    a_rows = [["value", "1", "3", "8", "9", "15"], ["cut", "L", "L", "|", "R", "R"]]
    b_headers = ["B", "0", "1", "2", "3", "4", "5"]
    b_rows = [["value", "7", "11", "18", "19", "21", "25"], ["cut", "L", "L", "L", "|", "R", "R"]]
    a_table = custom_array_table("Partition in A", a_headers, a_rows, {(1, 3): ACTION_BG})
    b_table = custom_array_table("Partition in B", b_headers, b_rows, {(1, 4): ACTION_BG})
    body = "\n".join(
        [
            f"a [shape=plain label=<{a_table}>];",
            f"b [shape=plain label=<{b_table}>];",
            note_node("bounds", "Boundary values", ["Aleft = 8, Aright = 9", "Bleft = 19, Bright = 21", "check Aleft <= Bright and Bleft <= Aright"], CLAIM_BG),
            note_node("direction", "Binary-search direction", ["if Aleft > Bright: move i left", "if Bleft > Aright: move i right"], ACTION_BG),
            "a -> bounds [style=invis];",
            "b -> bounds [style=invis];",
            "bounds -> direction [label=\"decides move\"];",
        ]
    )
    return wrap_graph(body, "4: search for the unique feasible partition", rankdir="TB")


def flatten_tree_graph() -> str:
    body = "\n".join(
        [
            'root [shape=circle style=filled fillcolor="#DBEAFE" label="1"];',
            'left [shape=circle style=filled fillcolor="#DBEAFE" label="2"];',
            'right [shape=circle style=filled fillcolor="#DBEAFE" label="5"];',
            'leftleft [shape=circle style=filled fillcolor="#DBEAFE" label="3"];',
            'leftright [shape=circle style=filled fillcolor="#DBEAFE" label="4"];',
            'rightright [shape=circle style=filled fillcolor="#DBEAFE" label="6"];',
            "root -> left; root -> right; left -> leftleft; left -> leftright; right -> rightright;",
            note_node("order", "Reverse preorder", ["visit 6 -> 5 -> 4 -> 3 -> 2 -> 1", "prev already stores the suffix", "that should follow the current node"], CLAIM_BG),
            'list [shape=record style="filled" fillcolor="#DCFCE7" label="1 | 2 | 3 | 4 | 5 | 6"];',
            "root -> order [style=dashed arrowhead=none];",
            "order -> list [label=\"rewire right pointers\"];",
        ]
    )
    return wrap_graph(body, "114: reverse preorder builds the flattened suffix", rankdir="TB")


def lru_cache_graph() -> str:
    body = "\n".join(
        [
            note_node("map", "Hash map", ["key 7 -> node7", "key 4 -> node4", "key 9 -> node9"], STATE_BG),
            note_node("list", "Recency list", ["head -> node9 -> node7 -> node4 -> tail", "MRU near head", "LRU near tail"], CLAIM_BG),
            note_node("ops", "Constant-time operations", ["lookup key in M", "remove / move node in the list", "evict tail.prev when full"], ACTION_BG),
            "map -> list [label=\"node pointers\"];",
            "list -> ops [label=\"supports promotion + eviction\"];",
        ]
    )
    return wrap_graph(body, "146: one map, one recency list")


def word_search_ii_graph() -> str:
    headers = ["", "0", "1", "2", "3"]
    rows = [
        ["0", "o", "a", "a", "n"],
        ["1", "e", "t", "a", "e"],
        ["2", "i", "h", "k", "r"],
    ]
    highlights = {(0, 1): ACTION_BG, (1, 1): ACTION_BG}
    table = custom_array_table("Board path example", headers, rows, highlights)
    body = "\n".join(
        [
            f'board [shape=plain label=<{table}>];',
            note_node("trie", "Trie path", ["root -> o -> a -> t", "terminal node stores \"oat\"", "missing child => prune the DFS branch"], CLAIM_BG),
            note_node("dedupe", "Output once", ["record the word", "clear only the terminal marker", "keep deeper shared prefixes intact"], ACTION_BG),
            "board -> trie [label=\"follow matching prefix\"];",
            "trie -> dedupe [label=\"when terminal is reached\"];",
        ]
    )
    return wrap_graph(body, "212: board DFS only survives along trie prefixes", rankdir="TB")


def make_visual(problem_dir: str, readme_text: str) -> str:
    custom = {
        "042-trapping-rain-water": trapping_rain_graph,
        "025-reverse-nodes-in-k-group": reverse_k_group_graph,
        "073-set-matrix-zeroes": set_matrix_zeroes_graph,
        "004-median-of-two-sorted-arrays": median_partition_graph,
        "114-flatten-binary-tree-to-linked-list": flatten_tree_graph,
        "146-lru-cache": lru_cache_graph,
        "212-word-search-ii": word_search_ii_graph,
    }
    if problem_dir in custom:
        return custom[problem_dir]()
    return generic_graph(problem_dir, readme_text)


def visual_block(problem_dir: str, title: str) -> str:
    custom = CUSTOM_VISUALS.get(problem_dir)
    visual_title = custom["title"] if custom else "Core Proof Map"
    alt = custom["alt"] if custom else f"Core proof map for {title}"
    followup = custom["followup"] if custom else (
        "This diagram compresses the state model, key claim, and algorithm consequence into one view so the proof spine is easier to reconstruct from memory."
    )
    return (
        "### Visuals\n\n"
        f"#### 1. {visual_title}\n"
        "This image is the required appendix visual for the note.\n\n"
        '<div align="center">\n'
        f'  <img src="png/visual_1.png" alt="{alt}">\n'
        "</div>\n\n"
        f"{followup}\n\n"
    )


def insert_visuals(readme_path: Path, problem_dir: str) -> None:
    current_text = readme_path.read_text()
    try:
        baseline = subprocess.run(
            ["git", "show", f"HEAD:{problem_dir}/README.md"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError:
        baseline = current_text

    title = read_title(baseline)
    block = visual_block(problem_dir, title)

    if "### Visuals" in baseline:
        updated = re.sub(
            r"### Visuals\n.*?(?=^### |\Z)",
            block,
            baseline,
            flags=re.M | re.S,
        )
    else:
        updated = baseline.replace("## Appendix\n\n", f"## Appendix\n\n{block}", 1)

    readme_path.write_text(updated)


def render(problem_dir: str, dot_content: str) -> None:
    dot_dir = ROOT / problem_dir / "dot"
    png_dir = ROOT / problem_dir / "png"
    dot_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)
    dot_path = dot_dir / "visual_1.dot"
    png_path = png_dir / "visual_1.png"
    dot_path.write_text(dot_content)
    subprocess.run(["dot", "-Tpng", str(dot_path), "-o", str(png_path)], check=True)


def main() -> None:
    for problem_dir in TARGETS:
        readme_path = ROOT / problem_dir / "README.md"
        readme_text = readme_path.read_text()
        dot = make_visual(problem_dir, readme_text)
        render(problem_dir, dot)
        insert_visuals(readme_path, problem_dir)
        print(f"updated {problem_dir}")


if __name__ == "__main__":
    main()
