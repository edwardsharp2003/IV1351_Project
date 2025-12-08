import os
import sys
import psycopg
from dotenv import load_dotenv

# Add the project root to the Python path to allow imports from `src`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dao import SchoolDAO
from src.model import (
    CourseLayout, CourseInstance, PlannedActivity, ActivityAllocation, Employee, SalaryHistory,
    Person, JobTitle, StudyPeriodType
)

def run_dao_test():
    # Go up one directory from `tests` to find the .env file in the project root
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if not all([db_host, db_port, db_user, db_password, db_name]):
        print("Error: One or more database environment variables are not set in .env file.")
        return

    conn = None
    try:
        conn = psycopg.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            dbname=db_name
        )
        print("Database connection established successfully.")

        dao = SchoolDAO(conn)
        print("SchoolDAO instantiated.")

        # Test data for Functionality 1
        test_course_code = 'IV1351'
        test_study_year = '2025'

        print(f"\n--- Testing get_data_for_course_cost_calculation for Course: {test_course_code}, Year: {test_study_year} ---")
        result = dao.get_data_for_course_cost_calculation(test_course_code, test_study_year)

        if result:
            course_layout, course_instance, planned_activities, allocations = result
            print("\nCourse Layout:")
            print(f"  {course_layout}")
            print("\nCourse Instance:")
            print(f"  {course_instance}")
            print(f"\nPlanned Activities ({len(planned_activities)}):")
            for pa in planned_activities:
                print(f"  {pa}")
            print(f"\nAllocations ({len(allocations)}):")
            for alloc_tuple in allocations:
                alloc, emp, sh, p, jt, st = alloc_tuple
                print(f"  Allocation: {alloc.id}, Employee: {p.first_name} {p.last_name} (ID: {emp.id}), Salary: {sh.salary_amount}")
        else:
            print(f"No data found for Course: {test_course_code}, Year: {test_study_year}")

    except psycopg.OperationalError as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during the test: {e}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    run_dao_test()
