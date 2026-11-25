import unittest
from review import rank, validate

CASE = {
    "case_id": "TEST-001",
    "user_prompt": "Dinner suggestion?",
    "context_turns": [{"turn_id": "T1", "text": "User likes simple Hindi."}],
    "responses": {"A": "Daal and rice.", "B": "You told me you have an allergy."},
    "annotations": {
        "A": {"scores": {"grounding": 5, "integration": 5, "helpfulness": 4}, "rationale": "Grounded", "evidence_turns": ["T1"]},
        "B": {"scores": {"grounding": 1, "integration": 1, "helpfulness": 1}, "rationale": "Unsupported allergy", "evidence_turns": ["T1"]}
    }
}


class TestEvaluation(unittest.TestCase):
    def test_ranking(self):
        self.assertEqual(rank(CASE)[0], "A")

    def test_missing_evidence(self):
        from copy import deepcopy
        case = deepcopy(CASE)
        case["annotations"]["A"]["evidence_turns"] = ["T99"]
        with self.assertRaises(ValueError):
            validate(case)

    def test_tie(self):
        from copy import deepcopy
        case = deepcopy(CASE)
        case["annotations"]["B"]["scores"] = dict(case["annotations"]["A"]["scores"])
        self.assertEqual(rank(case)[0], "Tie")


if __name__ == "__main__":
    unittest.main()
