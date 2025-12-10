import psycopg
from psycopg.rows import dict_row # To fetch rows as dictionaries
from typing import List, Tuple, Optional
from src.model import (
    CourseInstance, PlannedActivity, ActivityAllocation, Employee, SalaryHistory,
    CourseLayout, StudyPeriodType, Person, JobTitle
)

class SchoolDAO:
    """
    Handles all database operations for the school application, specifically
    focused on teaching and course-related data.
    """

    def __init__(self, db_connection):
        """
        Initializes the DAO with a database connection.

        :param db_connection: An active psycopg connection object.
        """
        self.conn = db_connection

    def get_data_for_course_cost_calculation(
        self, course_code: str, study_year: str
    ) -> Optional[Tuple[CourseLayout, CourseInstance, List[PlannedActivity], List[Tuple[ActivityAllocation, Employee, SalaryHistory, Person, JobTitle, StudyPeriodType]]]]:
        """
        Fetches all necessary raw data from the database to calculate teaching cost
        for a specific course instance. The data returned is to be processed by the
        controller layer.

        :param course_code: The code of the course (e.g., 'IV1351').
        :param study_year: The year the instance was held (e.g., '2025').
        :return: A tuple containing the CourseLayout, CourseInstance, a list of PlannedActivity DTOs,
                 and a list of tuples for ActivityAllocations (including Employee, SalaryHistory, Person, JobTitle, StudyPeriodType details).
                 Returns None if the course instance is not found.
        """

        # The connection's autocommit mode is now managed in main.py.
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                # 1. Find the specific course_layout and course_instance
                # This query also gets the period associated with the course_instance
                # We assume one course instance is associated with one period for simplicity
                # in this context, or we'd need to handle multiple periods.
                cursor.execute(
                    """
                    SELECT 
                        cl.course_layout_id, cl.course_code, cl.course_name, cl.min_students, cl.max_students, cl.hp, cl.valid_from,
                        ci.course_instance_id, ci.num_students, ci.study_year
                    FROM course_layout cl
                    JOIN course_instance ci ON cl.course_layout_id = ci.course_layout_id
                    WHERE cl.course_code = %s AND ci.study_year = %s
                    FOR UPDATE; -- Use SELECT FOR UPDATE as per assignment for transactional integrity
                    """,
                    (course_code, study_year)
                )
                course_data = cursor.fetchone()

                if not course_data:
                    self.conn.rollback()
                    return None

                course_layout_dto = CourseLayout(
                    id=course_data['course_layout_id'],
                    course_code=course_data['course_code'],
                    course_name=course_data['course_name'],
                    min_students=course_data['min_students'],
                    max_students=course_data['max_students'],
                    hp=course_data['hp'],
                    valid_from=course_data['valid_from']
                )
                course_instance_dto = CourseInstance(
                    id=course_data['course_instance_id'],
                    num_students=course_data['num_students'],
                    study_year=course_data['study_year'],
                    course_layout_id=course_data['course_layout_id']
                )
                
                course_instance_id = course_instance_dto.id

                # 2. Get planned activities for this course instance
                cursor.execute(
                    """
                    SELECT pa.teaching_activity_id, pa.course_instance_id, pa.study_period_id, pa.planned_hours,
                           ta.activity_name, ta.factor
                    FROM planned_activity pa
                    JOIN teaching_activity ta ON pa.teaching_activity_id = ta.teaching_activity_id
                    WHERE pa.course_instance_id = %s;
                    """,
                    (course_instance_id,)
                )
                planned_activities_raw = cursor.fetchall()
                planned_activities_dtos: List[PlannedActivity] = []
                for row in planned_activities_raw:
                    planned_activities_dtos.append(
                        PlannedActivity(
                            teaching_activity_id=row['teaching_activity_id'],
                            course_instance_id=row['course_instance_id'],
                            study_period_id=row['study_period_id'],
                            planned_hours=row['planned_hours']
                        )
                    )
                    # We could also return a DTO for TeachingActivity here if needed by controller

                # 3. Get actual allocations and employee details (including salary and person info)
                # This is a complex join to get all required details for actual cost calculation.
                cursor.execute(
                    """
                    SELECT
                        aa.activity_allocation_id, aa.employee_id, aa.teaching_activity_id, aa.course_instance_id, aa.study_period_id,
                        e.person_id, e.job_title_id, e.department_id, e.manager_id, e.salary_history_id,
                        sh.salary_amount, sh.valid_from AS salary_valid_from,
                        p.personal_number, p.first_name, p.last_name,
                        jt.job_title,
                        st.study_period_id AS period_id_from_study_type -- To ensure we get the period info if needed
                    FROM activity_allocation aa
                    JOIN employee e ON aa.employee_id = e.employee_id
                    JOIN salary_history sh ON e.salary_history_id = sh.salary_history_id
                    JOIN person p ON e.person_id = p.person_id
                    JOIN job_title jt ON e.job_title_id = jt.job_title_id
                    JOIN study_period_type st ON aa.study_period_id = st.study_period_id
                    WHERE aa.course_instance_id = %s;
                    """,
                    (course_instance_id,)
                )
                allocations_raw = cursor.fetchall()
                
                # We return a list of tuples, where each tuple contains the relevant DTOs
                # for an allocation. The controller will then process this.
                allocations_dtos: List[Tuple[ActivityAllocation, Employee, SalaryHistory, Person, JobTitle, StudyPeriodType]] = []
                for row in allocations_raw:
                    allocation = ActivityAllocation(
                        id=row['activity_allocation_id'],
                        employee_id=row['employee_id'],
                        teaching_activity_id=row['teaching_activity_id'],
                        course_instance_id=row['course_instance_id'],
                        study_period_id=row['study_period_id']
                    )
                    employee = Employee(
                        id=row['employee_id'],
                        person_id=row['person_id'],
                        job_title_id=row['job_title_id'],
                        department_id=row['department_id'],
                        manager_id=row['manager_id'],
                        salary_history_id=row['salary_history_id']
                    )
                    salary_history = SalaryHistory(
                        id=row['salary_history_id'],
                        salary_amount=row['salary_amount'],
                        valid_from=row['salary_valid_from'],
                        employee_id=row['employee_id']
                    )
                    person = Person(
                        id=row['person_id'],
                        personal_number=row['personal_number'],
                        first_name=row['first_name'],
                        last_name=row['last_name']
                    )
                    job_title = JobTitle(
                        id=row['job_title_id'],
                        job_title=row['job_title']
                    )
                    study_period = StudyPeriodType(
                        id=row['study_period_id'] # Use the original study_period_id from aa, not the alias
                    )

                    allocations_dtos.append((allocation, employee, salary_history, person, job_title, study_period))

            self.conn.commit()
            return course_layout_dto, course_instance_dto, planned_activities_dtos, allocations_dtos

        except psycopg.Error as e:
            self.conn.rollback()
            print(f"Database error in get_data_for_course_cost_calculation: {e}") # Log the error
            raise # Re-raise the exception after logging and rollback
        except Exception as e:
            self.conn.rollback()
            print(f"An unexpected error occurred: {e}") # Log other errors
            raise # Re-raise the exception after logging and rollback

    def update_student_count(self, course_code: str, study_year: str, student_change: int) -> bool:
        """
        Updates the number of students for a specific course instance.
        student_change: The number of students to add (can be negative)
        return True if the update was successful, False otherwise.
        """
        try:
            with self.conn.cursor() as cursor:
                # First, find the course_instance_id from the course_code and study_year.
                # We lock the row for the update.
                cursor.execute(
                    """
                    SELECT ci.course_instance_id FROM course_instance ci
                    JOIN course_layout cl ON ci.course_layout_id = cl.course_layout_id
                    WHERE cl.course_code = %s AND ci.study_year = %s
                    FOR UPDATE;
                    """,
                    (course_code, study_year)
                )
                instance = cursor.fetchone()

                if not instance:
                    self.conn.rollback()
                    return False # Course instance not found

                course_instance_id = instance[0]

                # Now, perform the update
                cursor.execute(
                    """
                    UPDATE course_instance
                    SET num_students = num_students + %s
                    WHERE course_instance_id = %s;
                    """,
                    (student_change, course_instance_id)
                )
                
                # Check if any row was actually updated
                if cursor.rowcount == 0:
                    self.conn.rollback()
                    return False

            self.conn.commit()
            return True

        except psycopg.Error as e:
            self.conn.rollback()
            print(f"Database error in update_student_count: {e}")
            raise
