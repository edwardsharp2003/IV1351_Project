from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

@dataclass
class StudyPeriodType:
    id: int

@dataclass
class CourseLayout:
    id: int
    course_code: str
    course_name: str
    min_students: int
    max_students: int
    hp: Decimal
    valid_from: date

@dataclass
class CourseInstance:
    id: int
    num_students: int
    study_year: str
    course_layout_id: int

@dataclass
class Person:
    id: int
    personal_number: str
    first_name: str
    last_name: str

@dataclass
class JobTitle:
    id: int
    job_title: str

@dataclass
class Department:
    id: int
    department_name: str
    manager_id: Optional[int]

@dataclass
class SalaryHistory:
    id: int
    salary_amount: Decimal
    valid_from: date
    employee_id: int

@dataclass
class Employee:
    id: int
    person_id: int
    job_title_id: int
    department_id: int
    manager_id: int
    salary_history_id: int

@dataclass
class Skill:
    id: int
    skill_name: str

@dataclass
class TeachingActivity:
    id: int
    activity_name: str
    factor: Decimal

@dataclass
class PlannedActivity:
    teaching_activity_id: int
    course_instance_id: int
    study_period_id: int
    planned_hours: int
    activity_name: str
    factor: Decimal

@dataclass
class ActivityAllocation:
    id: int
    employee_id: int
    teaching_activity_id: int
    course_instance_id: int
    study_period_id: int

# --- Composite DTO for specific functionality ---

@dataclass
class CourseTeachingCost:
    course_code: str
    course_instance_id: int
    period: int
    planned_cost_ksek: Decimal
    actual_cost_ksek: Decimal