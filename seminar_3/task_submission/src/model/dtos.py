from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CourseCost:
    course_code: str
    course_instance_id: int
    period: int
    planned_cost: Decimal
    actual_cost: Decimal