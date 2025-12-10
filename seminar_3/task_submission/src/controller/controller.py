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
        # Calculates the planned and actual teaching cost for a given course instance.

        # 1. Get all the raw data from the DAO
        dao_data = self.dao.get_data_for_course_cost_calculation(course_code, study_year)

        if not dao_data:
            return None  # Course instance not found

        course_layout, course_instance, planned_activities, allocations = dao_data

        # 2a. Sum hours from explicitly planned activities
        explicit_planned_hours = sum(pa.planned_hours * pa.factor for pa in planned_activities)
        # 2b. Calculate implicit Admin and Exam hours
        admin_hours = (2 * course_layout.hp) + 28 + (Decimal('0.2') * course_instance.num_students)
        exam_hours = 32 + (Decimal('0.725') * course_instance.num_students)
        # 2c. Calculate total hours and final planned cost
        total_planned_hours = explicit_planned_hours + admin_hours + exam_hours
        planned_cost = total_planned_hours * ASSUMED_HOURLY_COST_SEK

        # 3. Apply business logic: Calculate Actual Cost with Proportional Distribution
        total_actual_cost = Decimal('0.00')
        teacher_workload = {} # {teacher_id: {'base_hours': Decimal, 'hourly_rate': Decimal}}
        total_base_hours = Decimal('0.00')

        # 3a. First pass: Aggregate each teacher's base hours and find their hourly rate
        for alloc_tuple in allocations:
            allocation, employee, salary_history, person, job_title, study_period = alloc_tuple
            
            # Find the planned hours for this specific allocation
            for pa in planned_activities:
                if pa.teaching_activity_id == allocation.teaching_activity_id:
                    # Initialize teacher if not already in workload
                    if employee.id not in teacher_workload:
                        teacher_workload[employee.id] = {
                            'base_hours': Decimal('0.00'),
                            'hourly_rate': salary_history.salary_amount / HOURS_PER_MONTH if HOURS_PER_MONTH > 0 else Decimal('0.00')
                        }
                    # Add hours (including factor) to this teacher's workload
                    hours_for_activity = pa.planned_hours * pa.factor
                    teacher_workload[employee.id]['base_hours'] += hours_for_activity
                    total_base_hours += hours_for_activity
                    break
        
        # 3b. Second pass: Calculate each teacher's share of derived hours and total actual cost
        total_derived_hours = admin_hours + exam_hours
        
        for teacher_id, work in teacher_workload.items():
            # Cost of their base work
            base_work_cost = work['base_hours'] * work['hourly_rate']
            
            # Their share of the derived work
            proportion_of_work = (work['base_hours'] / total_base_hours) if total_base_hours > 0 else Decimal('0.00')
            derived_hours_for_teacher = total_derived_hours * proportion_of_work
            derived_work_cost = derived_hours_for_teacher * work['hourly_rate']
            
            # Total cost for this teacher is their base work + their share of derived work
            total_actual_cost += base_work_cost + derived_work_cost

        # 4. Create and return the final DTO
        period = 0
        if allocations:
            period = allocations[0][5].id
        elif planned_activities:
            period = planned_activities[0].study_period_id

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

    def allocate_hours(self, course_code: str, study_period_id: int, teaching_activity_id: int, planned_hours: int, employee_id: int, study_year: str) -> bool:
        """
        Allocates teaching hours for an employee on a specific course instance and activity.
        """
        try:
            return self.dao.allocate_hours(course_code, study_period_id, teaching_activity_id, planned_hours, employee_id, study_year)
        except Exception as e:
            print(f"An error occurred in the controller during allocation: {e}")
            return False

    def deallocate_hours(self, course_code: str, study_period_id: int, teaching_activity_id: int, employee_id: int, study_year: str) -> bool:
        """
        Deallocates teaching hours for an employee on a specific course instance and activity.
        """
        try:
            return self.dao.deallocate_hours(course_code, study_period_id, teaching_activity_id, employee_id, study_year)
        except Exception as e:
            print(f"An error occurred in the controller during deallocation: {e}")
            return False