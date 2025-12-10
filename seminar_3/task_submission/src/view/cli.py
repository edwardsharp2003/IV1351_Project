from src.model import CourseTeachingCost
from src.controller import Controller
from typing import Optional

class Cli:
    """
    Command Line Interface for the teaching allocation application.
    Handles all user interaction (input and output).
    """
    def __init__(self, controller: Controller):
        """
        Initializes the CLI with a controller instance.
        :param controller: An instance of the Controller.
        """
        self.controller = controller

    def start(self):
        """
        Starts the main loop of the CLI application.
        """
        while True:
            self._display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self._compute_teaching_cost_ui()
            elif choice == '2':
                self._modify_student_count_ui()
            elif choice == '3':
                self._allocate_deallocate_teaching_hours()
            elif choice == 'exit':
                print("Exiting application. Goodbye!")
                break
            else:
                if choice:
                    print("Invalid choice. Please try again.")

    def _display_menu(self):
        """
        Displays the main menu options to the user.
        """
        print("\n--- Teaching Allocation System ---")
        print("1. Compute Teaching Cost for a Course Instance")
        print("2. Modify Student Count for a Course Instance")
        print("3. Allocate and deallocate teaching loads:")
        print("Type 'exit' to quit.")
        print("----------------------------------")

    def _compute_teaching_cost_ui(self, course_code: str = None, study_year: str = None):
        """
        Handles the user interaction for computing teaching cost.
        Can be called with pre-filled course_code and study_year for post-update display.
        """
        if course_code is None:
            print("\n--- Compute Teaching Cost ---")
            course_code = input("Enter Course Code (e.g., IV1351): ").strip().upper()
            study_year = input("Enter Study Year (e.g., 2025): ").strip()
        else:
            print(f"\n--- Re-computing Teaching Cost for Course: {course_code}, Year: {study_year} ---")


        if not course_code or not study_year:
            print("Course Code and Study Year cannot be empty.")
            return

        try:
            result: Optional[CourseTeachingCost] = self.controller.get_course_teaching_cost(
                course_code, study_year
            )

            if result:
                print("\n--- Teaching Cost Report ---")
                print(f"{'Course Code':<15} {'Course Instance ID':<20} {'Period':<8} {'Planned Cost (KSEK)':<25} {'Actual Cost (KSEK)':<25}")
                print("-" * 93)
                print(f"{result.course_code:<15} {result.course_instance_id:<20} {result.period:<8} {result.planned_cost_ksek:<25.2f} {result.actual_cost_ksek:<25.2f}")
                print("-" * 93)
            else:
                print(f"No course instance found for Course Code '{course_code}' in Year '{study_year}'.")
        except Exception as e:
            print(f"An error occurred while computing teaching cost: {e}")

    def _modify_student_count_ui(self):
        print("\n--- Modify Student Count ---")
        course_code = input("Enter Course Code (e.g., IV1351): ").strip().upper()
        study_year = input("Enter Study Year (e.g., 2025): ").strip()
        
        try:
            student_change_str = input("Enter change in students (e.g., 100 to add 100, -50 to remove 50): ").strip()
            student_change = int(student_change_str)
        except ValueError:
            print("Invalid input for student change. Please enter an integer.")
            return

        if not course_code or not study_year:
            print("Course Code and Study Year cannot be empty.")
            return

        try:
            success = self.controller.update_student_count(course_code, study_year, student_change)
            if success:
                print(f"Successfully updated student count for {course_code} ({study_year}) by {student_change}.")
            else:
                print(f"Failed to update student count for {course_code} ({study_year}). Course instance might not exist.")
        except Exception as e:
            print(f"An error occurred while modifying student count: {e}")  
            
    def _allocate_deallocate_teaching_hours(self):
        """
        Handles the user interaction for computing teaching cost.
        """
        print("\n--- Choose between allocating of deallocating Teachers to a course_instance")
        print("\n 1. For allocating")
        print("\n 2. For deallocating")
        print("Type 'exit' to go to main menu.")
        print("----------------------------------")
        
        
        
        while True:
            self._display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self._allocate()
            elif choice == '2':
                self._deallocate()
            elif choice == 'exit':
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                
        
    def _allocate(self):
        print("funtion")
        
    def _deallocate(self):
        print("funtion")