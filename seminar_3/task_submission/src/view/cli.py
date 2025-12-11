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
            # Note: Calling _display_menu() here might be confusing as it shows the main menu options
            # but we are in a sub-menu. I'll just prompt for choice.
            choice = input("Enter your choice (1, 2, or exit): ").strip()

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
        print("\n--- Allocate Teaching Hours ---")
        
        course_code = input("Enter Course Code (e.g., IV1351): ").strip().upper()
        study_year = input("Enter Study Year (e.g., 2025): ").strip()
        
        if not course_code or not study_year:
            print("Course Code and Study Year cannot be empty.")
            return

        try:
            study_period_id = int(input("Enter Study Period ID (1-4): ").strip())
            employee_id = int(input("Enter Employee ID: ").strip())
            
            print("\nTeaching Activities:")
            print(" 1. Lecture")
            print(" 2. Lab")
            print(" 3. Seminar")
            print(" 4. Project")
            print(" 5. Tutorial Hours")
            print(" 6. Other")
            
            choice = int(input("Enter Teaching Activity from the list 1-6 (e.g., 2): ").strip())
            
            teaching_activity_id = None

            if choice == 6:
                # Call _other and wait for the new ID
                teaching_activity_id = self._other()
                if not teaching_activity_id:
                    print("Aborting allocation because the new activity could not be created.")
                    return
            else:
                teaching_activity_id = choice

            planned_hours = int(input("Enter Planned Hours: ").strip())
            
            print(f"\nAttempting to allocate {planned_hours} hours for Employee {employee_id}...")
            
            success = self.controller.allocate_hours(
                course_code, 
                study_period_id, 
                teaching_activity_id, 
                planned_hours, 
                employee_id, 
                study_year
            )
            
            if success:
                print("Allocation successful!")
                
                print("\n--- Updated Allocations for this Activity ---")
            activities = self.controller.get_all_teaching_activities(teaching_activity_id,employee_id,study_year)
            
            if activities:
                # Simple header
                print(f"{'Activity':<15} {'Course':<10} {'Year':<6} {'Hours':<6} {'Emp ID':<8}")
                print("-" * 50)
                for row in activities:
                    print(f"{row['activity_name']:<15} {row['course_code']:<10} {row['study_year']:<6} {row['planned_hours']:<6} {row['employee_id']:<8}")
                print("-" * 50)
            else:
                print("Allocation failed. Please check inputs or database logs.")
                
        except ValueError:
            print("Invalid input. Please enter numeric values for IDs and hours.")
        except Exception as e:
            print(f"An error occurred during allocation: {e}")
    
    def _deallocate(self):
        print("\n--- Deallocate Teaching Hours ---")
        
        course_code = input("Enter Course Code (e.g., IV1351): ").strip().upper()
        study_year = input("Enter Study Year (e.g., 2025): ").strip()
        
        if not course_code or not study_year:
            print("Course Code and Study Year cannot be empty.")
            return

        try:
            study_period_id = int(input("Enter Study Period ID (1-4): ").strip())
            employee_id = int(input("Enter Employee ID: ").strip())
            teaching_activity_id = int(input("Enter Teaching Activity type ").strip())
            
            print(f"\nAttempting to deallocate Employee {employee_id} from activity {teaching_activity_id}...")
            
            success = self.controller.deallocate_hours(
                course_code, 
                study_period_id, 
                teaching_activity_id, 
                employee_id, 
                study_year
            )
            
            if success:
                print("Deallocation successful!")
            else:
                print("Deallocation failed. Allocation might not exist.")
                
        except ValueError:
            print("Invalid input. Please enter numeric values for IDs.")
        except Exception as e:
            print(f"An error occurred during deallocation: {e}")

    def _other(self) -> Optional[int]:
        print("\n --- Choose the name of the Teaching Activity")
        try:
            other_teaching_activity = input("Enter the name of the new activity(e.g, Exercise):").strip()
            
            # Note: create_new_teaching_activity returns an ID (int) or None
            new_id = self.controller.create_new_teaching_activity(other_teaching_activity)
            
            if new_id: 
                print(f"New Teaching Activity created successfully with ID: {new_id}")
                return new_id
            else: 
                print("Creation of a new teaching activity failed.")
                return None
                
        except ValueError:
            print("Invalid input.")
            return None
        except Exception as e:
            print(f"An error occurred during creation: {e}")
            return None


