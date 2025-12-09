from decimal import Decimal
from src.dao import SchoolDAO
from src.model import CourseTeachingCost

# Define constants for calculation
HOURS_PER_MONTH = 160

class Controller:
    """
    Handles application logic, orchestrating calls between the view and the DAO.
    """
    def __init__(self, dao: SchoolDAO):
        """
        Initializes the Controller with a data access object.
        :param dao: An instance of SchoolDAO.
        """
        self.dao = dao

    def get_course_teaching_cost(self, course_code: str, study_year: str) -> CourseTeachingCost | None:
        """
        Calculates the planned and actual teaching cost for a given course instance.

        :param course_code: The code of the course (e.g., 'IV1351').
        :param study_year: The year of the course instance (e.g., '2025').
        :return: A CourseTeachingCost DTO with the calculated costs, or None if the course is not found.
        """
        # 1. Get all the raw data from the DAO
        dao_data = self.dao.get_data_for_course_cost_calculation(course_code, study_year)

        if not dao_data:
            return None # Course instance not found
        
        course_layout, course_instance, planned_activities, allocations = dao_data

        # 2. Apply business logic: Calculate Planned Cost
        # 2a. Get all teacher salaries from the DAO and compute the average.
        all_salaries = self.dao.get_all_teacher_salaries()
        average_monthly_salary = sum(all_salaries) / len(all_salaries) if all_salaries else 0
        average_hourly_cost = Decimal(average_monthly_salary / HOURS_PER_MONTH)

        # 2b. Use the dynamic average to calculate the planned cost.
        total_planned_hours = sum(pa.planned_hours for pa in planned_activities)
        planned_cost = total_planned_hours * average_hourly_cost

        # 3. Apply business logic: Calculate Actual Cost
        # For simplicity, we'll sum the monthly salaries of all unique allocated teachers.
        teacher_salaries = {alloc_tuple[1].id: alloc_tuple[2].salary_amount for alloc_tuple in allocations}
        total_actual_salary_sum = sum(teacher_salaries.values())

        # 4. Create and return the final DTO
        # The example output showed cost in KSEK, so we divide by 1000
        # Determine period from either allocations or planned activities
        period = 0
        if allocations:
            period = allocations[0][5].id # Accessing study_period_type DTO from the tuple
        elif planned_activities:
            period = planned_activities[0].study_period_id # Accessing study_period_id from PlannedActivity DTO

        result_dto = CourseTeachingCost(
            course_code=course_layout.course_code,
            course_instance_id=course_instance.id,
            period=period,
            planned_cost_ksek=round(planned_cost / 1000, 2),
            actual_cost_ksek=round(total_actual_salary_sum / 1000, 2)
        )
        
        return result_dto
