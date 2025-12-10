import random
import os
from faker import Faker

fake = Faker()

# CONFIGURATION
NUM_PEOPLE = 100
NUM_COURSES = 50

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(SCRIPT_DIR, "insert_data.sql")


def escape_sql(text: str) -> str:
    return text.replace("'", "''")


print(f"Generating data for NEW schema into {FILENAME}...")

with open(FILENAME, "w") as f:
    f.write("-- Generated Data Script (for updated schema with salary_history_id on employee)\n")
    f.write("-- NOTE: Run this on a clean database after running task1.sql\n\n")

    # ---------------------------------------------------------
    # 0. FIX CIRCULAR FK BETWEEN EMPLOYEE <-> SALARY_HISTORY
    # ---------------------------------------------------------
    f.write("-- Temporarily drop circular salary constraints (if they exist)\n")
    f.write("ALTER TABLE employee DROP CONSTRAINT IF EXISTS FK_employee_4;\n")
    f.write("ALTER TABLE salary_history DROP CONSTRAINT IF EXISTS FK_salary_history_0;\n\n")

    # ---------------------------------------------------------
    # 1. LOOKUP TABLES & INDEPENDENT DATA
    # ---------------------------------------------------------

    # Study Period Types (integer IDs)
    study_periods = [1, 2, 3, 4]
    f.write("-- Study Period Types\n")
    for sp in study_periods:
        f.write(f"INSERT INTO study_period_type (study_period_id) VALUES ({sp});\n")

    # Departments (manager_id set later to avoid FK issues)
    departments = ["Civil Engineering", "Information Technology", "Architecture", "Urban Planning"]
    f.write("\n-- Departments\n")
    for dept in departments:
        f.write(
            "INSERT INTO department (department_name, manager_id) "
            f"VALUES ('{dept}', NULL);\n"
        )

    # Job Titles
    job_titles = ["Lecturer", "Senior Lecturer", "Professor", "PhD Student", "Administrator"]
    f.write("\n-- Job Titles\n")
    for job in job_titles:
        f.write(f"INSERT INTO job_title (job_title) VALUES ('{job}');\n")

    # Skills
    skills = ["Python", "SQL", "AutoCAD", "Revit", "GIS", "Project Management", "Matlab"]
    f.write("\n-- Skills\n")
    for skill in skills:
        f.write(f"INSERT INTO skill (skill_name) VALUES ('{skill}');\n")

    # Teaching Activities
    teaching_activities = [("Lecture", 2.0), ("Lab", 1.7), ("Seminar", 1.5), ("Project", 0.5)]
    f.write("\n-- Teaching Activities\n")
    for name, factor in teaching_activities:
        f.write(
            "INSERT INTO teaching_activity (activity_name, factor) "
            f"VALUES ('{name}', {factor});\n"
        )

    # Course Layouts (with valid_from DATE)
    course_layouts = [
        ('AL1523', 'Digitalisation and Innovation for Sustainable Development', 7.5),
        ('DD1351', 'Logic for Computer Scientists', 7.5),
        ('DD2350', 'Algorithms, Data Structures and Complexity', 9.5),
        ('DD2352', 'Algorithms and Complexity', 7.5),
        ('DD2401', 'Neuroscience', 7.5),
        ('DH2642', 'Interaction Programming and the Dynamic Web', 7.5),
        ('EL1020', 'Automatic Control, general course', 6.0),
        ('EQ1110', 'Continuous Time Signals and Systems', 6.0),
        ('EQ1120', 'Discrete Time Signals and Systems', 6.0),
        ('IA150X', 'Degree Project in Information and Communication Technology', 15.0),
        ('ID1018', 'Programming I', 7.5),
        ('ID1021', 'Algorithms and Data Structures', 7.5),
        ('ID1206', 'Operating Systems', 7.5),
        ('ID1214', 'Artificial Intelligence and Applied Methods', 7.5),
        ('ID1217', 'Concurrent Programming', 7.5),
        ('ID2201', 'Distributed Systems, Basic Course', 7.5),
        ('ID2202', 'Compilers and Execution Environments', 7.5),
        ('ID2216', 'Developing Mobile Applications', 7.5),
        ('IE1204', 'Digital Design', 7.5),
        ('IE1206', 'Embedded Electronics', 7.5),
        ('II1303', 'Signal Processing', 7.5),
        ('II1305', 'Project in Information and Communication Technology', 7.5),
        ('II1307', 'Active Career', 1.5),
        ('II1308', 'Introduction to Programming', 1.5),
        ('IK1203', 'Networks and Communication', 7.5),
        ('IK1330', 'Wireless Systems', 7.5),
        ('IL1333', 'Hardware Security', 7.5),
        ('IS1200', 'Computer Hardware Engineering', 7.5),
        ('IS1300', 'Embedded Systems', 7.5),
        ('IS2202', 'Computer Systems Architecture', 7.5),
        ('IV1013', 'Introduction to Computer Security', 7.5),
        ('IV1350', 'Object Oriented Design', 7.5),
        ('IV1351', 'Data Storage Paradigms', 7.5),
        ('LS1601', 'Intercultural competence', 4.5),
        ('LS2442', 'English for Employment', 7.5),
        ('ME1003', 'Industrial Management, Basic Course', 6.0),
        ('ME2016', 'Project Management: Leadership and Control', 6.0),
        ('ME2163', 'Leading People and Organizations in Different Contexts', 6.0),
        ('SF1546', 'Numerical Methods, Basic Course', 6.0),
        ('SF1610', 'Discrete Mathematics', 7.5),
        ('SF1624', 'Algebra and Geometry', 7.5),
        ('SF1625', 'Calculus in One Variable', 7.5),
        ('SF1633', 'Differential Equations I', 6.0),
        ('SF1683', 'Differential Equations and Transforms', 9.0),
        ('SF1686', 'Calculus in Several Variable', 7.5),
        ('SF1689', 'Basic Course in Mathematics', 6.0),
        ('SF1912', 'Probability Theory and Statistics', 6.0),
        ('SG1102', 'Mechanics, Smaller Course', 6.0),
        ('SH1011', 'Modern Physics', 7.5),
        ('SK1118', 'Electromagnetism and Waves', 7.5),
    ]
    f.write("\n-- Course Layouts\n")
    for code, name, hp in course_layouts:
        min_s = random.randint(50, 150)
        max_s = random.randint(150, 300)
        valid_from = "2020-01-01"
        f.write(
            "INSERT INTO course_layout (course_code, course_name, min_students, max_students, hp, valid_from) "
            f"VALUES ('{code}', '{name}', {min_s}, {max_s}, {hp}, DATE '{valid_from}');\n"
        )

    # ---------------------------------------------------------
    # 2. PEOPLE, ADDRESSES, PHONES, EMPLOYEES
    # ---------------------------------------------------------
    f.write("\n-- People, Employees, Phones, Addresses\n")

    # We rely on identity columns to assign:
    # person_id       = 1..NUM_PEOPLE   (order of insert)
    # employee_id     = 1..NUM_PEOPLE   (order of insert)
    # salary_history_id = 1..NUM_PEOPLE (order of insert later)
    #
    # We will set:
    #   employee.salary_history_id = i
    #   salary_history.employee_id = i
    # so that when we re-add the FKs, the circular relation is valid.

    for i in range(1, NUM_PEOPLE + 1):
        # Person
        sex = random.choice(["M", "F"])
        fn = fake.first_name_male() if sex == "M" else fake.first_name_female()
        ln = fake.last_name_male() if sex == "M" else fake.last_name_female()

        # personal_number = yymmdd-xxxx (CHAR(11))
        year = random.randint(1950, 2002)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # always valid
        suffix = random.randint(0, 9999)
        p_num = f"{year % 100:02d}{month:02d}{day:02d}-{suffix:04d}"

        f.write(
            "INSERT INTO person (personal_number, first_name, last_name) "
            f"VALUES ('{p_num}', '{escape_sql(fn)}', '{escape_sql(ln)}');\n"
        )

        # Address & Phone
        addr = escape_sql(fake.address().replace("\n", ", "))
        phone = fake.phone_number()
        f.write(
            f"INSERT INTO address (person_id, address) VALUES ({i}, '{addr}');\n"
        )
        f.write(
            f"INSERT INTO phone (person_id, phone_number) VALUES ({i}, '{phone}');\n"
        )

        # Employee
        dept_id = random.randint(1, len(departments))
        job_id = random.randint(1, len(job_titles))

        # manager_id is NOT NULL and FK to employee(employee_id).
        # For employee i, we choose a manager between 1 and i (self-manager allowed).
        mgr_id = random.randint(1, i)

        # salary_history_id will be i (we'll insert matching salary_history rows later)
        salary_hist_id = i

        f.write(
            "INSERT INTO employee (person_id, job_title_id, department_id, manager_id, salary_history_id) "
            f"VALUES ({i}, {job_id}, {dept_id}, {mgr_id}, {salary_hist_id});\n"
        )

    # ---------------------------------------------------------
    # 3. SALARY HISTORY (paired 1:1 with employees)
    # ---------------------------------------------------------
    f.write("\n-- Salary History\n")
    # We assume:
    #  - employee_id for employees is 1..NUM_PEOPLE
    #  - salary_history_id will be 1..NUM_PEOPLE in insert order (identity)
    for emp_id in range(1, NUM_PEOPLE + 1):
        salary = random.randint(30000, 65000)
        f.write(
            "INSERT INTO salary_history (salary_amount, valid_from, employee_id) "
            f"VALUES ({salary}, DATE '2024-01-01', {emp_id});\n"
        )

    # ---------------------------------------------------------
    # 4. COURSE INSTANCES & COURSE_INSTANCE_PERIOD
    # ---------------------------------------------------------
    f.write("\n-- Course Instances\n")

    # Define the range of years to generate instances for
    years_to_generate = range(2015, 2026)  # 2015 to 2025 inclusive

    num_total_instances = len(course_layouts) * len(years_to_generate)
    course_instances = list(range(1, num_total_instances + 1))

    for year in years_to_generate:
        year_str = str(year)
        # The layout_id is 1-based, matching the assumed identity/serial column for course_layout
        for layout_id in range(1, len(course_layouts) + 1):
            num_studs = random.randint(15, 80)
            f.write(
                "INSERT INTO course_instance (num_students, study_year, course_layout_id) "
                f"VALUES ({num_studs}, '{year_str}', {layout_id});\n"
            )

    f.write("\n-- Course Instance Periods\n")
    # For each course_instance, create exactly one period row.
    # course_instance_period.course_instance_id is IDENTITY, and has FK to course_instance.
    # Because both tables are empty and we insert NUM_INSTANCES rows in each,
    # their IDs will both be 1..NUM_INSTANCES and the FK will be satisfied.
    #
    # We track a "logical" ci_id (1..NUM_INSTANCES) which corresponds to the identity value.
    course_instance_periods = []  # list of dicts {ci_id, sp_id}
    for ci_id in course_instances:
        sp_id = random.choice(study_periods)
        f.write(
            f"INSERT INTO course_instance_period (study_period_id) VALUES ({sp_id});\n"
        )
        course_instance_periods.append({"ci_id": ci_id, "sp_id": sp_id})

    # ---------------------------------------------------------
    # 5. EMPLOYEE SKILLS
    # ---------------------------------------------------------
    f.write("\n-- Employee Skills\n")
    for emp_id in range(1, NUM_PEOPLE + 1):
        num_emp_skills = random.randint(1, 3)
        chosen_skill_ids = random.sample(
            range(1, len(skills) + 1), num_emp_skills
        )
        for skill_id in chosen_skill_ids:
            f.write(
                f"INSERT INTO employee_skill (employee_id, skill_id) "
                f"VALUES ({emp_id}, {skill_id});\n"
            )

    # ---------------------------------------------------------
    # 6. PLANNED ACTIVITIES (linked to course_instance_period)
    # ---------------------------------------------------------
    f.write("\n-- Planned Activities\n")

    # Structure: planned_activity(teaching_activity_id, course_instance_id, study_period_id, planned_hours)
    # FK to course_instance_period(course_instance_id, study_period_id).
    planned_activities = []  # list of dicts {ci_id, ta_id, sp_id}

    for cip in course_instance_periods:
        ci_id = cip["ci_id"]   # logical course_instance_id (1..NUM_INSTANCES)
        sp_id = cip["sp_id"]
        ta_id = random.randint(1, len(teaching_activities))
        hours = random.randint(10, 50)

        f.write(
            "INSERT INTO planned_activity (teaching_activity_id, course_instance_id, study_period_id, planned_hours) "
            f"VALUES ({ta_id}, {ci_id}, {sp_id}, {hours});\n"
        )

        planned_activities.append({"ci_id": ci_id, "ta_id": ta_id, "sp_id": sp_id})

    # ---------------------------------------------------------
    # 7. ACTIVITY ALLOCATIONS (linked to planned_activity)
    # ---------------------------------------------------------
    f.write("\n-- Activity Allocations\n")

    # Track teacher workload: {(emp_id, sp_id): {course_instance_id, ...}}
    teacher_workload = {}

    for pa in planned_activities:
        ta_id = pa["ta_id"]
        sp_id = pa["sp_id"]
        ci_id = pa["ci_id"]

        # For each planned activity, try to assign 1 or 2 teachers
        num_teachers_to_assign = random.randint(1, 2)

        # Find eligible teachers who have not exceeded their course limit for this period
        all_possible_emp_ids = list(range(1, NUM_PEOPLE + 1))
        random.shuffle(all_possible_emp_ids)

        assigned_teachers_count = 0
        for emp_id in all_possible_emp_ids:
            # Get the set of courses this teacher is already assigned to in this period
            courses_in_period = teacher_workload.get((emp_id, sp_id), set())

            # A teacher is eligible if they are assigned to fewer than 4 courses in this period,
            # OR if the current course is one they are already assigned to (prevents double-counting).
            if len(courses_in_period) < 4 or ci_id in courses_in_period:
                # Assign this teacher
                f.write(
                    "INSERT INTO activity_allocation (employee_id, teaching_activity_id, course_instance_id, study_period_id) "
                    f"VALUES ({emp_id}, {ta_id}, {ci_id}, {sp_id});\n"
                )

                # Update their workload
                teacher_workload.setdefault((emp_id, sp_id), set()).add(ci_id)

                assigned_teachers_count += 1
                if assigned_teachers_count >= num_teachers_to_assign:
                    break  # Found enough teachers for this activity

        if assigned_teachers_count < num_teachers_to_assign:
            print(f"WARNING: Could only assign {assigned_teachers_count} out of {num_teachers_to_assign} teachers for activity on course instance {ci_id} due to workload limits.")

    # ---------------------------------------------------------
    # 8. SET DEPARTMENT MANAGERS (AFTER EMPLOYEES EXIST)
    # ---------------------------------------------------------
    f.write("\n-- Update Departments Manager\n")
    for dep_id in range(1, len(departments) + 1):
        mgr_id = random.randint(1, NUM_PEOPLE)
        f.write(
            f"UPDATE department SET manager_id = {mgr_id} "
            f"WHERE department_id = {dep_id};\n"
        )

    # ---------------------------------------------------------
    # 9. RE-ADD CIRCULAR SALARY CONSTRAINTS
    # ---------------------------------------------------------
    f.write("\n-- Re-add circular salary constraints\n")
    f.write(
        "ALTER TABLE salary_history "
        "ADD CONSTRAINT FK_salary_history_0 FOREIGN KEY (employee_id) REFERENCES employee (employee_id);\n"
    )
    f.write(
        "ALTER TABLE employee "
        "ADD CONSTRAINT FK_employee_4 FOREIGN KEY (salary_history_id) REFERENCES salary_history (salary_history_id);\n"
    )

print(f"Done! Created {FILENAME}")