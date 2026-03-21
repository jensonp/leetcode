import os
import subprocess

os.makedirs("dot", exist_ok=True)
os.makedirs("png", exist_ok=True)

def render(name, dot_content):
    with open(f"dot/{name}.dot", "w") as f:
        f.write(dot_content)
    subprocess.run(["dot", "-Tpng", f"dot/{name}.dot", "-o", f"png/{name}.png"])

# 1. Setup
setup_content = """digraph G {
rankdir=LR;
node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 1 |<f1> 2 |<f2> 3 |<f3> 0 |<f4> 0 |<f5> 0 ", fillcolor=lightblue, style=filled];
nums2 [label="<f0> 2 |<f1> 5 |<f2> 6 ", fillcolor=lightyellow, style=filled];
m [shape=plaintext, label="m = 3"]; m -> nums1:f1;
n [shape=plaintext, label="n = 3"]; n -> nums2:f1;
buffer [shape=plaintext, label="buffer (size n = 3)"]; buffer -> nums1:f4;
labelloc="t"; label="Problem Setup: nums1 has m valid elements and a buffer of size n"; fontsize=14;
}"""
render("setup", setup_content)

# 2. Brute Force naive appending
bf_content = """digraph G {
rankdir=TB;
node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 1 |<f1> 2 |<f2> 3 |<f3> 2 |<f4> 5 |<f5> 6", fillcolor=salmon, style=filled];
nums2 [label="<f0> 2 |<f1> 5 |<f2> 6", fillcolor=lightyellow, style=filled];
edge [color=red];
nums2:f0 -> nums1:f3;
nums2:f1 -> nums1:f4;
nums2:f2 -> nums1:f5;
note [shape=plaintext, label="O((N)) append... BUT O((m+n)log(m+n)) Sort required after append!\\nIgnores existing sorted property entirely.", fontcolor=red];
labelloc="t"; label="Brute Force: Append and Re-sort"; fontsize=14;
}"""
render("bruteforce", bf_content)

# 3. Pointer Transitions (Step 0 to Step 4)
def generate_step(step, nums1, nums2, p1, p2, p, action_text):
    dot_content = f"""digraph G {{
    rankdir=TB;
    node [shape=record, fontname="Helvetica", style=filled, fillcolor=white];
    nums1 [label="{ '|'.join(f'<f{i}> {val}' for i, val in enumerate(nums1)) }", fillcolor=lightblue];
    nums2 [label="{ '|'.join(f'<f{i}> {val}' for i, val in enumerate(nums2)) }", fillcolor=lightyellow];
    node [shape=plaintext, fillcolor=none, fontcolor=blue, fontname="Helvetica-Bold"];
    """
    if p1 >= 0:
        dot_content += f'p1 [label="p1={p1}"]; p1 -> nums1:f{p1};\n'
    if p2 >= 0:
        dot_content += f'p2 [label="p2={p2}"]; p2 -> nums2:f{p2};\n'
    if p >= 0:
        dot_content += f'p [label="p={p}"]; p -> nums1:f{p} [color=red, fontcolor=red];\n'
    dot_content += f'    labelloc="t";\n    label="{action_text}";\n    fontsize=14;\n}}\n'
    render(f"step{step}", dot_content)

n1 = [1, 2, 3, 0, 0, 0]
n2 = [2, 5, 6]
p1, p2, p = 2, 2, 5

generate_step(0, n1, n2, p1, p2, p, "Optimal Step 0: Pointers initialized at tails")

steps_done = 0
while p2 >= 0:
    steps_done += 1
    if p1 >= 0 and n1[p1] > n2[p2]:
        val = n1[p1]; n1[p] = val; p1 -= 1
        action = f"Placed nums1[p1] ({val}) at nums1[p]"
    else:
        val = n2[p2]; n1[p] = val; p2 -= 1
        action = f"Placed nums2[p2] ({val}) at nums1[p]"
    generate_step(steps_done, n1, n2, p1, p2, p, action)
    p -= 1

# 4. Invariant Preservation
inv_content = """digraph G {
rankdir=TB;
node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 1 |<f1> 2 |<f2> 3 |<f3> 5 |<f4> 6 |<f5> x", fillcolor=lightgrey, style=filled];
p [shape=plaintext, label="p = 3"]; p -> nums1:f3 [color=red];
p1 [shape=plaintext, label="p1 = 1"]; p1 -> nums1:f1 [color=blue];
note [shape=plaintext, label="Processed: (m-1-p1) + (n-1-p2) = 1 + 2 = 3\\nFilled space: (m+n-1) - p = 5 - 3 = 2", fontcolor=purple];
labelloc="t"; label="Invariant: Filled space matches elements parsed.\\np will never collide visually with p1"; fontsize=14;
}"""
render("invariant", inv_content)

# 5. Edge Case
edge_content = """digraph G {
rankdir=TB;
node [shape=record, fontname="Helvetica"];
nums1 [label="<f0> 0 |<f1> 0 |<f2> 0", fillcolor=lightgrey, style=filled];
nums2 [label="<f0> 1 |<f1> 2 |<f2> 3", fillcolor=lightyellow, style=filled];
p1 [shape=plaintext, label="p1 = -1 (exhausted immediately)"];
p2 [shape=plaintext, label="p2 = 2"]; p2 -> nums2:f2;
p [shape=plaintext, label="p = 2"]; p -> nums1:f2;
edge [color=green, style=dashed];
nums2:f2 -> nums1:f2;
labelloc="t"; label="Edge Case: m=0\\np1 starts exhausted, so nums2 is blindly copied into nums1 safely."; fontsize=14;
}"""
render("edge_case", edge_content)

print("Generated all visualizations!")
