from dataclasses import dataclass


@dataclass
class Student:
    registration_no: str
    first_name: str
    last_name: str
    gender: str
    dob: str
    email: str
    phone: str
    address: str
    course_id: int
    semester: int
    admission_date: str
    photo_path: str = ""