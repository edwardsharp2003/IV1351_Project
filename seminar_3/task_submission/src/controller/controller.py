from decimal import Decimal
from src.dao import SchoolDAO
from src.model import CourseTeachingCost

ASSUMED_HOURLY_COST_SEK = Decimal('300.00')  # an assumed hourly cost for planned cost calculation
HOURS_PER_MONTH = 160  # used for average teacher salary calculation


class Controller:
    # Handles application logic, orchestrating calls between the view and the DAO.
    def __init__(self, dao: SchoolDAO):
        # Initializes the Controller with a dao, an instance of SchoolDAO
        self.dao = dao

    def get_course_teaching_cost(self, course_code: str, study_year: str) -> CourseTeachingCost | None:
        """
        Calculates the planned and actual teaching cost for a given course instance.

        :param course_code: e.g. 'IV1351'
        :param study_year: e.g. '2025'
        :return: A CourseTeachingCost DTO with the calculated costs, or None if the course is not found.
        """
        # 1. Get all the raw data from the DAO
        dao_data = self.dao.get_data_for_course_cost_calculation(course_code, study_year)

        if not dao_data:
            return None  # Course instance not found

        course_layout, course_instance, planned_activities, allocations = dao_data

        # 2. Apply business logic: Calculate Planned Cost using the new detailed formula
        
        # 2a. Sum hours from explicitly planned activities (Lectures, Labs, etc.)
        explicit_planned_hours = sum(pa.planned_hours * pa.factor for pa in planned_activities)

        # 2b. Calculate implicit hours for Admin and Exam based on formulas
        # Admin hours formula: (2 * hp + 28 + 0.2 * num_students)
        admin_hours = (2 * course_layout.hp) + 28 + (Decimal('0.2') * course_instance.num_students)
        
        # Exam hours formula: (32 + 0.725 * num_students)
        exam_hours = 32 + (Decimal('0.725') * course_instance.num_students)

        # 2c. Calculate total hours and final planned cost
        total_hours = explicit_planned_hours + admin_hours + exam_hours
        planned_cost = total_hours * ASSUMED_HOURLY_COST_SEK


        # 3. Apply business logic: Calculate Actual Cost
        total_actual_cost = Decimal('0.00')

        # We need to ensure we don't double count if multiple allocations point to same planned activity,
        # but the current model suggests one allocation per activity for an employee.

        for alloc_tuple in allocations:
            allocation, employee, salary_history, person, job_title, study_period = alloc_tuple

            # Get the teacher's individual hourly rate from their monthly salary
            teacher_monthly_salary = salary_history.salary_amount
            # Ensure division by zero is handled if HOURS_PER_MONTH is 0 or if salary is huge.
            teacher_hourly_rate = teacher_monthly_salary / HOURS_PER_MONTH if HOURS_PER_MONTH > 0 else Decimal('0.00')

            # Find the planned hours for the specific activity this allocation refers to
            # This assumes there's a corresponding PlannedActivity entry for each ActivityAllocation.
            matching_planned_activity_hours = 0
            for pa in planned_activities:
                if pa.teaching_activity_id == allocation.teaching_activity_id and \
                        pa.course_instance_id == allocation.course_instance_id and \
                        pa.study_period_id == allocation.study_period_id:
                    matching_planned_activity_hours = pa.planned_hours
                    break

            # Add to total actual cost based on their hourly rate and the hours of their allocated activity
            total_actual_cost += teacher_hourly_rate * matching_planned_activity_hours

        # 4. Create and return the final DTO
        # The example output showed cost in KSEK, so we divide by 1000
        period = 0
        if allocations:
            period = allocations[0][5].id  # Accessing study_period_type DTO from the tuple
        elif planned_activities:
            period = planned_activities[0].study_period_id  # Accessing study_period_id from PlannedActivity DTO

        result_dto = CourseTeachingCost(
            course_code=course_layout.course_code,
            course_instance_id=course_instance.id,
            period=period,
            planned_cost_ksek=round(planned_cost / 1000, 2),
            actual_cost_ksek=round(total_actual_cost / 1000, 2)
        )

        return result_dto

    def update_student_count(self, course_code: str, study_year: str, student_change: int) -> bool:
        """
        Passes the request to update student count to the DAO.

        :param course_code: The code of the course.
        :param study_year: The year of the course instance.
        :param student_change: The number of students to add (can be negative).
        :return: True if successful, False otherwise.
        """
        try:
            return self.dao.update_student_count(course_code, study_year, student_change)
        except Exception as e:
            # In a real application, you might have more specific error handling here
            print(f"An error occurred in the controller: {e}")
            return False

