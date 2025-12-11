# Expose all DTOs directly from the model-package for cleaner imports.
from .dtos import (
    StudyPeriodType,
    CourseLayout,
    CourseInstance,
    Person,
    JobTitle,
    Department,
    SalaryHistory,
    Employee,
    Skill,
    TeachingActivity,
    PlannedActivity,
    ActivityAllocation,
    CourseTeachingCost,
)

# Expose business logic services
from .logic import CostCalculator
