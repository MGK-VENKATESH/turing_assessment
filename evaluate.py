import json
from answerer import ask  # make sure this imports your function

# -------------------------
# Load 8 questions
# -------------------------
with open("8_questions.json", "r") as f:
    questions = json.load(f)

results = []

# -------------------------
# Evaluate each question
# -------------------------
for q in questions:
    baseline = ask(q, k=5, mode="baseline") or {}
    hybrid = ask(q, k=5, mode="hybrid") or {}

    # Safely get scores
    baseline_score = baseline.get('score', 0) 
    hybrid_score = hybrid.get('score', 0)
    improved = hybrid_score > baseline_score

    # Get answers or indicate abstain
    baseline_answer = baseline.get('answer') or 'ABSTAIN'
    hybrid_answer = hybrid.get('answer') or 'ABSTAIN'

    results.append({
        "question": q,
        "baseline_answer": baseline_answer,
        "baseline_score": baseline_score,
        "hybrid_answer": hybrid_answer,
        "hybrid_score": hybrid_score,
        "improved": improved
    })

# -------------------------
# Write Markdown table
# -------------------------
md_lines = [
    "| Question | Baseline Answer | Baseline Score | Hybrid Answer | Hybrid Score | Improved? |",
    "|----------|----------------|----------------|---------------|--------------|-----------|"
]

for r in results:
    # truncate long answers for display
    baseline_display = (r['baseline_answer'][:50] + "...") if r['baseline_answer'] != 'ABSTAIN' else 'ABSTAIN'
    hybrid_display = (r['hybrid_answer'][:50] + "...") if r['hybrid_answer'] != 'ABSTAIN' else 'ABSTAIN'

    md_lines.append(
        f"| {r['question']} | {baseline_display} | {r['baseline_score']:.3f} | {hybrid_display} | {r['hybrid_score']:.3f} | {r['improved']} |"
    )

with open("results_table.md", "w") as f:
    f.write("\n".join(md_lines))

print("✅ Evaluation complete. See results_table.md for the table.")

