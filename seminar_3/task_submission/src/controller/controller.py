from src.dao import SchoolDAO
from src.model import CourseTeachingCost
from src.model.logic import CostCalculator


class Controller:
    def __init__(self, dao: SchoolDAO):
        self.dao = dao

    def get_course_teaching_cost(self, course_code: str, study_year: str) -> CourseTeachingCost | None:

        # 1. Get all the raw data from the DAO
        dao_data = self.dao.get_data_for_course_cost_calculation(course_code, study_year)

        if not dao_data:
            return None  # Course instance not found

        course_layout, course_instance, planned_activities, allocations = dao_data

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
            #missing an error handler
            
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
            
            return False

    def create_new_teaching_activity(self, other_teaching_activity: str):
        """
        Creating a new teaching activity
        """
        try:
            return self.dao.create_new_teaching_activity(other_teaching_activity)
        except Exception as e:
            
            return False

    def get_all_teaching_activities(self, teaching_activity_id: int, employee_id: int, study_year: str):
        """
        Retrieves all teaching activities.
        """
        try:
            return self.dao.get_all_teaching_activities(teaching_activity_id, employee_id, study_year)
        except Exception as e:
            
            return []
