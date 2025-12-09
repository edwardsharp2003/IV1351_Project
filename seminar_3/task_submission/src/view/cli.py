from src.model import CourseTeachingCost # Assuming CourseTeachingCost is the primary output DTO
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
            elif choice == 'exit':
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def _display_menu(self):
        """
        Displays the main menu options to the user.
        """
        print("\n--- Teaching Allocation System ---")
        print("1. Compute Teaching Cost for a Course Instance")
        print("Type 'exit' to quit.")
        print("----------------------------------")

    def _compute_teaching_cost_ui(self):
        """
        Handles the user interaction for computing teaching cost.
        """
        print("\n--- Compute Teaching Cost ---")
        course_code = input("Enter Course Code (e.g., IV1351): ").strip().upper()
        study_year = input("Enter Study Year (e.g., 2025): ").strip()

        if not course_code or not study_year:
            print("Course Code and Study Year cannot be empty.")
            return

        try:
            result: Optional[CourseTeachingCost] = self.controller.get_course_teaching_cost(
                course_code, study_year
            )

            if result:
                print("\n--- Teaching Cost Report ---")
                print(f"{'Course Code':<15} {'Course Instance':<20} {'Period':<8} {'Planned Cost (KSEK)':<25} {'Actual Cost (KSEK)':<25}")
                print("-" * 93)
                print(f"{result.course_code:<15} {result.course_instance_id:<20} {result.period:<8} {result.planned_cost_ksek:<25.2f} {result.actual_cost_ksek:<25.2f}")
                print("-" * 93)
            else:
                print(f"No course instance found for Course Code '{course_code}' in Year '{study_year}'.")
        except Exception as e:
            print(f"An error occurred while computing teaching cost: {e}")
