from dataclasses import dataclass


@dataclass
class Course:
    course_code: str
    course_name: str
    duration_months: int
    total_semesters: int
    annual_fee: float
    status: str