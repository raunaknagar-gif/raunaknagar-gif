"""Synthetic rules-only AI AR follow-up quality checker; no live payer calling."""
from dataclasses import dataclass, field

REQUIRED = {
    "pending": ("received_date", "turnaround_time"),
    "paid_eft": ("amount", "eft_number", "issue_date", "cleared_date", "bank_last_four"),
    "paid_check": ("amount", "check_number", "issue_date", "cleared_date", "pay_to_address"),
    "corrected": ("submission_method",),
    "appeal": ("appeal_method", "filing_limit", "appeal_address_or_portal"),
    "denied": ("denial_reason", "next_action"),
}


@dataclass
class FollowUp:
    scenario: str
    facts: dict = field(default_factory=dict)
    already_asked: set = field(default_factory=set)

    def missing(self) -> list[str]:
        if self.scenario not in REQUIRED:
            raise ValueError("Unsupported scenario: " + self.scenario)
        return [key for key in REQUIRED[self.scenario] if not self.facts.get(key)]

    def next_question(self):
        for key in self.missing():
            if key not in self.already_asked:
                self.already_asked.add(key)
                return f"Please confirm {key.replace('_', ' ')}."
        return None

    def record(self, key: str, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("A non-empty fact is required")
        self.facts[key] = value.strip()

    def summary(self):
        return {
            "scenario": self.scenario,
            "complete": not self.missing(),
            "missing_fields": self.missing(),
            "facts": self.facts,
        }


if __name__ == "__main__":
    example = FollowUp("pending", {"received_date": "2026-11-02"})
    print(example.summary())
    print("Next question:", example.next_question())
