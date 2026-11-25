import unittest
from engine import FollowUp


class TestFollowUp(unittest.TestCase):
    def test_pending_requirements(self):
        case = FollowUp("pending", {"received_date": "2026-11-02"})
        self.assertEqual(case.missing(), ["turnaround_time"])

    def test_anti_repetition(self):
        case = FollowUp("corrected")
        self.assertEqual(case.next_question(), "Please confirm submission method.")
        self.assertIsNone(case.next_question())

    def test_complete_appeal(self):
        case = FollowUp("appeal", {
            "appeal_method": "portal",
            "filing_limit": "90 days",
            "appeal_address_or_portal": "payer portal",
        })
        self.assertTrue(case.summary()["complete"])

    def test_eft_requires_bank_details(self):
        case = FollowUp("paid_eft", {"amount": "100", "eft_number": "TEST123",
                                      "issue_date": "2026-11-01", "cleared_date": "2026-11-02"})
        self.assertIn("bank_last_four", case.missing())


if __name__ == "__main__":
    unittest.main()
