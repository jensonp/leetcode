import os
import subprocess

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
        
    dot_content += f'    labelloc="t";\n    label="{action_text}";\n    fontsize=14;\n'
    dot_content += "}\n"
    
    name = f"step{step}"
    with open(f"{name}.dot", "w") as f:
        f.write(dot_content)
    subprocess.run(["dot", "-Tpng", f"{name}.dot", "-o", f"{name}.png"])

nums1 = [1, 2, 3, 0, 0, 0]
m = 3
nums2 = [2, 5, 6]
n = 3

p1 = m - 1
p2 = n - 1
p = m + n - 1

step = 0
generate_step(step, nums1, nums2, p1, p2, p, "Step 0: Initial State\\nBoth arrays start sorted. Pointers p1 and p2 at the end of valid elements.\\nPointer p at the very end of nums1 (the write position).")

while p2 >= 0:
    step += 1
    if p1 >= 0 and nums1[p1] > nums2[p2]:
        val = nums1[p1]
        action = f"Step {step}: nums1[p1] ({val}) > nums2[p2] ({nums2[p2]})\\nPlace {val} at nums1[p], move p1 and p left"
        nums1[p] = val
        p1 -= 1
    else:
        val = nums2[p2]
        action = f"Step {step}: nums2[p2] ({val}) >= nums1[p1]\\nPlace {val} at nums1[p], move p2 and p left"
        nums1[p] = val
        p2 -= 1
    generate_step(step, nums1, nums2, p1, p2, p, action)
    p -= 1

print(f"Generated {step + 1} image states.")
