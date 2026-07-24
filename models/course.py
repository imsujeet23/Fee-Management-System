from dataclasses import dataclass


@dataclass
class Course:
    course_code: str
    course_name: str
    duration: str
    total_semesters: int
    annual_fee: float
    status: str