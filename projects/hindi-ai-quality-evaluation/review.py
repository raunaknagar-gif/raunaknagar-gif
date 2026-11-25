"""Evidence-based Hindi side-by-side QA annotation reader; ratings entered by humans."""
import json
import sys
from pathlib import Path

CRITERIA = ("grounding", "integration", "helpfulness")


def validate(review):
    required = ("case_id", "user_prompt", "context_turns", "responses", "annotations")
    if not isinstance(review, dict) or any(k not in review for k in required):
        raise ValueError("Missing required case fields")
    turns = review["context_turns"]
    if not isinstance(turns, list) or not turns:
        raise ValueError("Missing context")
    ids = {turn.get("turn_id") for turn in turns}
    if None in ids or len(ids) != len(turns):
        raise ValueError("Invalid or duplicate context IDs")
    if set(review["responses"]) != {"A", "B"} or set(review["annotations"]) != {"A", "B"}:
        raise ValueError("Need A and B responses and annotations")
    for key in ("A", "B"):
        ann = review["annotations"][key]
        if not isinstance(review["responses"][key], str) or not review["responses"][key].strip():
            raise ValueError("Empty response")
        if set(ann["scores"]) != set(CRITERIA):
            raise ValueError("All three score fields required")
        if any(type(ann["scores"][c]) is not int or not 1 <= ann["scores"][c] <= 5 for c in CRITERIA):
            raise ValueError("Score out of range")
        if not ann.get("rationale") or not ann.get("evidence_turns"):
            raise ValueError("Evidence and rationale required")
        if not set(ann["evidence_turns"]).issubset(ids):
            raise ValueError("Invalid evidence turn")


def rank(review):
    validate(review)
    totals = {k: sum(review["annotations"][k]["scores"].values()) for k in ("A", "B")}
    winner = "Tie" if totals["A"] == totals["B"] else max(totals, key=totals.get)
    return winner, totals


def display(review):
    winner, totals = rank(review)
    output = [f"Case: {review['case_id']}", f"User request: {review['user_prompt']}"]
    for key in ("A", "B"):
        ann = review["annotations"][key]
        output.append(f"Response {key} — {totals[key]}/15 | {ann['scores']}")
        output.append(f"Evidence: {', '.join(ann['evidence_turns'])}")
        output.append(f"Reason: {ann['rationale']}")
    return "\n".join(output + [f"Preferred: {winner} (human ratings)"])


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("examples/hindi_recipe.json")
    try:
        print(display(json.loads(path.read_text(encoding="utf-8"))))
    except (ValueError, KeyError, OSError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
