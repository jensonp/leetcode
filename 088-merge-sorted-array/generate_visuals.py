import os
import subprocess

os.makedirs("dot", exist_ok=True)
os.makedirs("png", exist_ok=True)

def render(name, dot_content):
    with open(f"dot/{name}.dot", "w") as f:
        f.write(dot_content)
    subprocess.run(["dot", "-Tpng", f"dot/{name}.dot", "-o", f"png/{name}.png"])

# 1. Problem Layout — physical vs logical data in nums1
render("layout", """digraph G {
rankdir=LR; node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 1 |<f1> 2 |<f2> 3 |<f3> 0 |<f4> 0 |<f5> 0", style=filled, fillcolor=lightblue];
nums2 [label="<f0> 2 |<f1> 5 |<f2> 6", style=filled, fillcolor=lightyellow];
valid [shape=plaintext, label="valid data (m=3)"]; valid -> nums1:f1;
cap [shape=plaintext, label="writable capacity (n=3)"]; cap -> nums1:f4;
labelloc="t"; label="Physical layout: first m slots are data, last n slots are capacity"; fontsize=14;
}""")

# 2. Brute force — why append+sort wastes work
render("bruteforce", """digraph G {
rankdir=TB; node [shape=record, fontname="Helvetica"];
before [label="1 | 2 | 3 | 0 | 0 | 0", style=filled, fillcolor=lightblue];
after_copy [label="1 | 2 | 3 | 2 | 5 | 6", style=filled, fillcolor=salmon];
after_sort [label="1 | 2 | 2 | 3 | 5 | 6", style=filled, fillcolor=lightgreen];
before -> after_copy [label="copy nums2 into tail"];
after_copy -> after_sort [label="sort entire array\\nO((m+n) log(m+n))"];
waste [shape=plaintext, label="Wastes the existing sorted order!", fontcolor=red];
labelloc="t"; label="Brute Force: Append + Sort"; fontsize=14;
}""")

# 3. Front merge — why shifting is expensive
render("front_shift", """digraph G {
rankdir=TB; node [shape=record, fontname="Helvetica"];
step0 [label="<f0> 1 |<f1> 2 |<f2> 3 |<f3> _ |<f4> _ |<f5> _", style=filled, fillcolor=lightblue];
nums2 [label="<f0> 0 |<f1> 0 |<f2> 0", style=filled, fillcolor=lightyellow];
step1 [label="<f0> 0 |<f1> 1 |<f2> 2 |<f3> 3 |<f4> _ |<f5> _", style=filled, fillcolor=salmon];
nums2 -> step0:f0 [label="insert 0 at front", color=red];
step0 -> step1 [label="shift ALL 3 elements right\\nO(m) per insertion!", color=red];
labelloc="t"; label="Front Merge: Every insertion shifts the entire block"; fontsize=14;
}""")

# 4-8. Step-by-step pointer transitions (5 diagrams)
def gen_step(step, n1, n2, i, j, k, action):
    dot = f"""digraph G {{
    rankdir=TB; node [shape=record, fontname="Helvetica", style=filled, fillcolor=white];
    nums1 [label="{'|'.join(f'<f{idx}> {v}' for idx, v in enumerate(n1))}", fillcolor=lightblue];
    nums2 [label="{'|'.join(f'<f{idx}> {v}' for idx, v in enumerate(n2))}", fillcolor=lightyellow];
    node [shape=plaintext, fillcolor=none, fontname="Helvetica-Bold"];
    """
    if i >= 0:
        dot += f'i [label="i={i}", fontcolor=blue]; i -> nums1:f{i};\n'
    else:
        dot += f'i [label="i=-1 (exhausted)", fontcolor=gray];\n'
    if j >= 0:
        dot += f'j [label="j={j}", fontcolor=darkgreen]; j -> nums2:f{j};\n'
    else:
        dot += f'j [label="j=-1 (done)", fontcolor=gray];\n'
    if k >= 0:
        dot += f'k [label="k={k}", fontcolor=red]; k -> nums1:f{k} [color=red];\n'
    dot += f'labelloc="t"; label="{action}"; fontsize=14;\n}}\n'
    render(f"step{step}", dot)

n1 = [1, 2, 3, 0, 0, 0]; n2 = [2, 5, 6]
i, j, k = 2, 2, 5
gen_step(0, n1, n2, i, j, k, "Step 0: Pointers initialized — i at end of A, j at end of B, k at end of nums1")

steps = 0
while j >= 0:
    steps += 1
    if i >= 0 and n1[i] > n2[j]:
        v = n1[i]; n1[k] = v; i -= 1
        act = f"Step {steps}: A[i]={v} > B[j]={n2[j] if j>=0 else '?'} — write {v} at k={k}, decrement i"
    else:
        v = n2[j]; n1[k] = v; j -= 1
        act = f"Step {steps}: B[j]={v} >= A[i]={n1[i] if i>=0 else 'exhausted'} — write {v} at k={k}, decrement j"
    gen_step(steps, n1, n2, i, j, k, act)
    k -= 1

# 9. Safety invariant — k never overtakes i
render("safety", """digraph G {
rankdir=TB; node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 1 |<f1> 2 |<f2> _ |<f3> 3 |<f4> 5 |<f5> 6", style=filled, fillcolor=lightblue];
i [shape=plaintext, label="i = 1", fontcolor=blue]; i -> nums1:f1;
k [shape=plaintext, label="k = 2", fontcolor=red]; k -> nums1:f2 [color=red];
gap [shape=plaintext, label="gap = k - i = n - x\\nHere: 2 - 1 = 3 - 2 = 1 >= 0\\nk can never overtake i", fontcolor=purple];
labelloc="t"; label="Safety: k - i = n - x >= 0 always holds"; fontsize=14;
}""")

# 10. Edge case — m=0, all of nums2 copied
render("edge_m0", """digraph G {
rankdir=TB; node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 0 |<f1> 0 |<f2> 0", style=filled, fillcolor=lightgrey];
nums2 [label="<f0> 1 |<f1> 2 |<f2> 3", style=filled, fillcolor=lightyellow];
result [label="<f0> 1 |<f1> 2 |<f2> 3", style=filled, fillcolor=lightgreen];
i [shape=plaintext, label="i = -1 (exhausted immediately)"]; 
j [shape=plaintext, label="j = 2"]; j -> nums2:f2;
k [shape=plaintext, label="k = 2"]; k -> nums1:f2;
nums1 -> result [label="loop copies all of B", style=dashed, color=green];
labelloc="t"; label="Edge Case: m=0 — i starts exhausted, B copied directly"; fontsize=14;
}""")

# 11. Edge case — n=0, nothing happens
render("edge_n0", """digraph G {
rankdir=TB; node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 1 |<f1> 2 |<f2> 3", style=filled, fillcolor=lightgreen];
nums2 [label="(empty)", shape=plaintext];
j [shape=plaintext, label="j = -1 immediately"]; 
note [shape=plaintext, label="Loop never executes.\\nnums1 is already the answer.", fontcolor=darkgreen];
labelloc="t"; label="Edge Case: n=0 — loop guard j>=0 is false, nothing happens"; fontsize=14;
}""")

print("Done! Generated all visuals.")
