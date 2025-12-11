from src.dao import SchoolDAO
from src.model import CourseTeachingCost
from src.model.logic import CostCalculator


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

        # 2. Delegate business logic to the model layer
        return CostCalculator.calculate_teaching_cost(
            course_layout,
            course_instance,
            planned_activities,
            allocations
        )

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

    def allocate_hours(self, course_code: str, study_period_id: int, teaching_activity_id: int, planned_hours: int,
                       employee_id: int, study_year: str) -> bool:
        """
        Allocates teaching hours for an employee on a specific course instance and activity.
        """
        try:
            return self.dao.allocate_hours(course_code, study_period_id, teaching_activity_id, planned_hours,
                                           employee_id, study_year)
        except Exception as e:
            print(f"An error occurred in the controller during allocation: {e}")
            return False

    def deallocate_hours(self, course_code: str, study_period_id: int, teaching_activity_id: int, employee_id: int,
                         study_year: str) -> bool:
        """
        Deallocates teaching hours for an employee on a specific course instance and activity.
        """
        try:
            return self.dao.deallocate_hours(course_code, study_period_id, teaching_activity_id, employee_id,
                                             study_year)
        except Exception as e:
            print(f"An error occurred in the controller during deallocation: {e}")
            return False

    def create_new_teaching_activity(self, other_teaching_activity: str):
        """
        Creating a new teaching activity
        """
        try:
            return self.dao.create_new_teaching_activity(other_teaching_activity)
        except Exception as e:
            print(f"An error occurred in the controller during deallocation: {e}")
            return False

    def get_all_teaching_activities(self, teaching_activity_id: int, employee_id: int, study_year: str):
        """
        Retrieves all teaching activities.
        """
        try:
            return self.dao.get_all_teaching_activities(teaching_activity_id, employee_id, study_year)
        except Exception as e:
            print(f"An error occurred in the controller while fetching activities: {e}")
            return []
