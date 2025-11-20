import random
from faker import Faker

fake = Faker()

# CONFIGURATION
NUM_PEOPLE = 50
NUM_COURSES = 10
NUM_INSTANCES = 30
FILENAME = "insert_data.sql"


def escape_sql(text: str) -> str:
    return text.replace("'", "''")


print(f"Generating data for NEW schema into {FILENAME}...")

with open(FILENAME, "w") as f:
    f.write("-- Generated Data Script V2 (for updated schema)\n")
    f.write("-- Note: Run this on a clean database (DROP/CREATE first)\n\n")

    # ---------------------------------------------------------
    # 1. LOOKUP TABLES & INDEPENDENT DATA
    # ---------------------------------------------------------

    # Study Period Types (now just integer IDs)
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
    teaching_activities = [("Lecture", 1.0), ("Lab", 2.0), ("Seminar", 1.5), ("Project", 0.5)]
    f.write("\n-- Teaching Activities\n")
    for name, factor in teaching_activities:
        f.write(
            "INSERT INTO teaching_activity (activity_name, factor) "
            f"VALUES ('{name}', {factor});\n"
        )

    # Course Layouts (now with valid_from DATE)
    course_layouts = [
        ("CE101", "Intro to Civil Engineering"),
        ("IT202", "Databases for Engineers"),
        ("CE305", "Structural Analysis"),
        ("IT301", "BIM Data Management"),
        ("CE400", "Geotechnical Engineering"),
        ("IT101", "Programming in Python"),
        ("CE202", "Fluid Mechanics"),
        ("AT105", "CAD Fundamentals"),
        ("UP201", "Urban GIS Systems"),
        ("CE500", "Master Thesis Project"),
    ]
    f.write("\n-- Course Layouts\n")
    for code, name in course_layouts:
        hp = random.choice([7.5, 15.0])
        min_s = random.randint(10, 20)
        max_s = random.randint(30, 100)
        valid_from = "2020-01-01"
        f.write(
            "INSERT INTO course_layout (course_code, course_name, min_students, max_students, hp, valid_from) "
            f"VALUES ('{code}', '{name}', {min_s}, {max_s}, {hp}, DATE '{valid_from}');\n"
        )

    # ---------------------------------------------------------
    # 2. PEOPLE, ADDRESSES, PHONES, EMPLOYEES
    # ---------------------------------------------------------
    f.write("\n-- People, Employees, Phones, Addresses\n")

    for i in range(1, NUM_PEOPLE + 1):
        # Person
        sex = random.choice(["M", "F"])
        fn = fake.first_name_male() if sex == "M" else fake.first_name_female()
        ln = fake.last_name_male() if sex == "M" else fake.last_name_female()

        # personal_number = yymmdd-xxxx (CHAR(11))
        year = random.randint(1950, 2002)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # keep always valid
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

        # Employee (no salary here anymore!)
        dept_id = random.randint(1, len(departments))
        job_id = random.randint(1, len(job_titles))
        # First 5 employees have no manager; others get a manager among 1..5
        mgr_id = "NULL" if i <= 5 else random.randint(1, 5)

        f.write(
            "INSERT INTO employee (person_id, job_title_id, department_id, manager_id) "
            f"VALUES ({i}, {job_id}, {dept_id}, {mgr_id});\n"
        )

    # ---------------------------------------------------------
    # 3. SALARY HISTORY (new table)
    # ---------------------------------------------------------
    f.write("\n-- Salary History\n")
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

    # We'll assume course_instance_id will be 1..NUM_INSTANCES in insert order
    course_instances = list(range(1, NUM_INSTANCES + 1))

    for _ci in course_instances:
        layout_id = random.randint(1, len(course_layouts))
        num_studs = random.randint(15, 80)
        year_str = "2024"
        f.write(
            "INSERT INTO course_instance (num_students, study_year, course_layout_id) "
            f"VALUES ({num_studs}, '{year_str}', {layout_id});\n"
        )

    f.write("\n-- Course Instance Periods\n")
    # For each course_instance, create exactly one period row
    course_instance_periods = []  # list of dicts {ci_id, sp_id}
    for ci_id in course_instances:
        sp_id = random.choice(study_periods)
        # course_instance_id is IDENTITY here, so we only insert study_period_id
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

    # We'll create exactly one planned_activity per course_instance_period,
    # relying on identity sequences to line up with course_instance_period IDs.
    planned_activities = []  # list of dicts {ci_id, ta_id, sp_id}

    for cip in course_instance_periods:
        ci_id = cip["ci_id"]  # logical ID, not written explicitly
        sp_id = cip["sp_id"]
        ta_id = random.randint(1, len(teaching_activities))
        hours = random.randint(10, 50)

        # course_instance_id in this table is IDENTITY; we omit it.
        f.write(
            "INSERT INTO planned_activity (teaching_activity_id, study_period_id, planned_hours) "
            f"VALUES ({ta_id}, {sp_id}, {hours});\n"
        )

        planned_activities.append({"ci_id": ci_id, "ta_id": ta_id, "sp_id": sp_id})

    # ---------------------------------------------------------
    # 7. ACTIVITY ALLOCATIONS (linked to planned_activity)
    # ---------------------------------------------------------
    f.write("\n-- Activity Allocations\n")

    # We'll create exactly one allocation per planned_activity,
    # again relying on identity sequences lining up row-by-row.
    for pa in planned_activities:
        emp_id = random.randint(1, NUM_PEOPLE)
        ta_id = pa["ta_id"]
        sp_id = pa["sp_id"]

        # activity_allocation_id and course_instance_id are IDENTITY columns;
        # we omit them and only set the FK columns we control.
        f.write(
            "INSERT INTO activity_allocation (employee_id, teaching_activity_id, study_period_id) "
            f"VALUES ({emp_id}, {ta_id}, {sp_id});\n"
        )

    # ---------------------------------------------------------
    # 8. CLEANUP CIRCULAR DEPENDENCY: SET DEPARTMENT MANAGERS
    # ---------------------------------------------------------
    f.write("\n-- Update Departments Manager\n")
    for dep_id in range(1, len(departments) + 1):
        mgr_id = random.randint(1, NUM_PEOPLE)
        f.write(
            f"UPDATE department SET manager_id = {mgr_id} "
            f"WHERE department_id = {dep_id};\n"
        )

print(f"Done! Created {FILENAME}")