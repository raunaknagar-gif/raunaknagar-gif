"""People OS local demonstration. Uses only fictional employee records."""
from dataclasses import dataclass, asdict
import json


@dataclass
class Employee:
    employee_id: str
    name: str
    department: str
    monthly_base: float


def calculate_pay(base, bonus=0.0, deduction=0.0):
    if any(x < 0 for x in (base, bonus, deduction)):
        raise ValueError("Amounts cannot be negative")
    gross = round(base + bonus, 2)
    net = round(gross - deduction, 2)
    if net < 0:
        raise ValueError("Deductions exceed earnings")
    return {"gross": gross, "deductions": deduction, "net": net}


def sample():
    person = Employee("DEMO-001", "Example Employee", "Operations", 30000.0)
    return {"employee": asdict(person),
            "payroll": calculate_pay(person.monthly_base, bonus=1500, deduction=500)}


if __name__ == "__main__":
    print(json.dumps(sample(), indent=2))
