from decimal import Decimal
from typing import List, Tuple
from .dtos import (
    CourseLayout, CourseInstance, PlannedActivity, ActivityAllocation,
    Employee, SalaryHistory, Person, JobTitle, StudyPeriodType,
    CourseTeachingCost
)


class CostCalculator:
    """
    Handles all business logic related to teaching cost calculations.
    This class is part of the model layer and contains no data access logic.
    """
    
    ASSUMED_HOURLY_COST_SEK = Decimal('300.00')
    HOURS_PER_MONTH = 160

    @staticmethod
    def calculate_teaching_cost(
        course_layout: CourseLayout,
        course_instance: CourseInstance,
        planned_activities: List[PlannedActivity],
        allocations: List[Tuple[ActivityAllocation, Employee, SalaryHistory, Person, JobTitle, StudyPeriodType]]
    ) -> CourseTeachingCost:
        """
        Calculates both planned and actual teaching costs for a course instance.
        
        :param course_layout: The course layout DTO
        :param course_instance: The course instance DTO
        :param planned_activities: List of planned activities
        :param allocations: List of tuples containing allocation and related employee data
        :return: CourseTeachingCost DTO with calculated costs
        """
        
        # 1. Calculate explicit planned hours from activities
        explicit_planned_hours = CostCalculator._calculate_explicit_planned_hours(planned_activities)
        
        # 2. Calculate implicit derived hours (Admin and Exam)
        admin_hours, exam_hours = CostCalculator._calculate_derived_hours(
            course_layout, 
            course_instance
        )
        
        # 3. Calculate total planned cost
        total_planned_hours = explicit_planned_hours + admin_hours + exam_hours
        planned_cost = total_planned_hours * CostCalculator.ASSUMED_HOURLY_COST_SEK
        
        # 4. Calculate actual cost with proportional distribution
        total_actual_cost = CostCalculator._calculate_actual_cost(
            planned_activities,
            allocations,
            admin_hours,
            exam_hours
        )
        
        # 5. Determine the period
        period = CostCalculator._determine_period(allocations, planned_activities)
        
        # 6. Create and return the result DTO
        return CourseTeachingCost(
            course_code=course_layout.course_code,
            course_instance_id=course_instance.id,
            period=period,
            planned_cost_ksek=round(planned_cost / 1000, 2),
            actual_cost_ksek=round(total_actual_cost / 1000, 2)
        )

    @staticmethod
    def _calculate_explicit_planned_hours(planned_activities: List[PlannedActivity]) -> Decimal:
        """
        Calculates the total explicit planned hours (including multiplication factors).
        """
        return sum(
            Decimal(str(pa.planned_hours)) * pa.factor 
            for pa in planned_activities
        )

    @staticmethod
    def _calculate_derived_hours(
        course_layout: CourseLayout, 
        course_instance: CourseInstance
    ) -> Tuple[Decimal, Decimal]:
        """
        Calculates implicit Admin and Exam hours based on business rules.
        
        :return: Tuple of (admin_hours, exam_hours)
        """
        admin_hours = (2 * course_layout.hp) + 28 + (Decimal('0.2') * course_instance.num_students)
        exam_hours = 32 + (Decimal('0.725') * course_instance.num_students)
        return admin_hours, exam_hours

    @staticmethod
    def _calculate_actual_cost(
        planned_activities: List[PlannedActivity],
        allocations: List[Tuple[ActivityAllocation, Employee, SalaryHistory, Person, JobTitle, StudyPeriodType]],
        admin_hours: Decimal,
        exam_hours: Decimal
    ) -> Decimal:
        """
        Calculates the actual cost by distributing base work and derived hours
        proportionally among allocated teachers.
        
        :return: Total actual cost in SEK
        """
        teacher_workload = {}  # {teacher_id: {'base_hours': Decimal, 'hourly_rate': Decimal}}
        total_base_hours = Decimal('0.00')
        
        # First pass: Aggregate each teacher's base hours and hourly rate
        for alloc_tuple in allocations:
            allocation, employee, salary_history, person, job_title, study_period = alloc_tuple
            
            # Find the planned hours for this specific allocation
            for pa in planned_activities:
                if pa.teaching_activity_id == allocation.teaching_activity_id:
                    # Initialize teacher if not already in workload
                    if employee.id not in teacher_workload:
                        hourly_rate = (
                            salary_history.salary_amount / CostCalculator.HOURS_PER_MONTH 
                            if CostCalculator.HOURS_PER_MONTH > 0 
                            else Decimal('0.00')
                        )
                        teacher_workload[employee.id] = {
                            'base_hours': Decimal('0.00'),
                            'hourly_rate': hourly_rate
                        }
                    
                    # Add hours (including factor) to this teacher's workload
                    hours_for_activity = Decimal(str(pa.planned_hours)) * pa.factor
                    teacher_workload[employee.id]['base_hours'] += hours_for_activity
                    total_base_hours += hours_for_activity
                    break
        
        # Second pass: Calculate each teacher's share of derived hours and total cost
        total_derived_hours = admin_hours + exam_hours
        total_actual_cost = Decimal('0.00')
        
        for teacher_id, work in teacher_workload.items():
            # Cost of their base work
            base_work_cost = work['base_hours'] * work['hourly_rate']
            
            # Their share of the derived work
            proportion_of_work = (
                (work['base_hours'] / total_base_hours) 
                if total_base_hours > 0 
                else Decimal('0.00')
            )
            derived_hours_for_teacher = total_derived_hours * proportion_of_work
            derived_work_cost = derived_hours_for_teacher * work['hourly_rate']
            
            # Total cost for this teacher is their base work + their share of derived work
            total_actual_cost += base_work_cost + derived_work_cost
        
        return total_actual_cost

    @staticmethod
    def _determine_period(
        allocations: List[Tuple[ActivityAllocation, Employee, SalaryHistory, Person, JobTitle, StudyPeriodType]],
        planned_activities: List[PlannedActivity]
    ) -> int:
        """
        Determines the study period from allocations or planned activities.
        
        :return: The study period ID, or 0 if none found
        """
        if allocations:
            return allocations[0][5].id
        elif planned_activities:
            return planned_activities[0].study_period_id
        return 0