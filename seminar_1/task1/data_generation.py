import random
from faker import Faker

fake = Faker()

# CONFIGURATION
NUM_PEOPLE = 50
NUM_COURSES = 10
NUM_INSTANCES = 30
FILENAME = "insert_data_v2.sql"


def escape_sql(text):
    return text.replace("'", "''")


print(f"Generating data for NEW schema into {FILENAME}...")

with open(FILENAME, "w") as f:
    f.write("-- Generated Data Script V2\n")
    f.write("-- Note: Run this on a clean database (DROP/CREATE first)\n\n")

    # ---------------------------------------------------------
    # 1. LOOKUP TABLES & INDEPENDENT DATA
    # ---------------------------------------------------------

    # Study Period Types (Using Integers as requested in schema)
    # 1=P1, 2=P2, 3=P3, 4=P4, 5=P1-P2
    valid_periods = [1, 2, 3, 4]
    f.write("-- Study Period Types\n")
    for p in valid_periods:
        f.write(f"INSERT INTO study_period_type (study_period_name) VALUES ({p});\n")

    # Departments
    departments = ["Civil Engineering", "Information Technology", "Architecture", "Urban Planning"]
    f.write("\n-- Departments\n")
    for dept in departments:
        f.write(f"INSERT INTO department (department_name, manager_id) VALUES ('{dept}', NULL);\n")

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
    # We need to track IDs manually since we don't know what DB assigns,
    # but we assume sequential 1..N for this script to work.
    teaching_activities = [("Lecture", 1.0), ("Lab", 2.0), ("Seminar", 1.5), ("Project", 0.5)]
    f.write("\n-- Teaching Activities\n")
    for name, factor in teaching_activities:
        f.write(f"INSERT INTO teaching_activity (activity_name, factor) VALUES ('{name}', {factor});\n")

    # Course Layouts
    course_layouts = [
        ("CE101", "Intro to Civil Engineering"), ("IT202", "Databases for Engineers"),
        ("CE305", "Structural Analysis"), ("IT301", "BIM Data Management"),
        ("CE400", "Geotechnical Engineering"), ("IT101", "Programming in Python"),
        ("CE202", "Fluid Mechanics"), ("AT105", "CAD Fundamentals"),
        ("UP201", "Urban GIS Systems"), ("CE500", "Master Thesis Project")
    ]
    f.write("\n-- Course Layouts\n")
    for code, name in course_layouts:
        hp = random.choice([7.5, 15.0])
        min_s = random.randint(10, 20)
        max_s = random.randint(30, 100)
        f.write(
            f"INSERT INTO course_layout (course_code, course_name, min_students, max_students, hp) VALUES ('{code}', '{name}', {min_s}, {max_s}, {hp});\n")

    # ---------------------------------------------------------
    # 2. PEOPLE & EMPLOYEES
    # ---------------------------------------------------------
    f.write("\n-- People, Employees, Phones, Addresses\n")

    for i in range(1, NUM_PEOPLE + 1):
        # Person
        sex = random.choice(['M', 'F'])
        fn = fake.first_name_male() if sex == 'M' else fake.first_name_female()
        ln = fake.last_name_male() if sex == 'M' else fake.last_name_female()
        p_num = f"{random.randint(1980, 2002)}{random.randint(10, 12)}{random.randint(10, 28)}-{random.randint(1000, 9999)}"

        f.write(
            f"INSERT INTO person (personal_number, first_name, last_name) VALUES ('{p_num}', '{escape_sql(fn)}', '{escape_sql(ln)}');\n")

        # Address & Phone
        addr = escape_sql(fake.address().replace("\n", ", "))
        phone = fake.phone_number()
        f.write(f"INSERT INTO address (person_id, address) VALUES ({i}, '{addr}');\n")
        f.write(f"INSERT INTO phone (person_id, phone_number) VALUES ({i}, '{phone}');\n")

        # Employee
        salary = random.randint(30000, 65000)
        dept_id = random.randint(1, len(departments))
        job_id = random.randint(1, len(job_titles))
        mgr_id = "NULL" if i <= 5 else random.randint(1, 5)  # First 5 are top managers

        f.write(
            f"INSERT INTO employee (salary, person_id, job_title_id, department_id, manager_id) VALUES ({salary}, {i}, {job_id}, {dept_id}, {mgr_id});\n")

    # ---------------------------------------------------------
    # 3. COURSE INSTANCES (Composite Key Prep)
    # ---------------------------------------------------------
    f.write("\n-- Course Instances\n")

    # We must track (instance_id, study_period) pairs to link Planned Activities later
    # Since IDs are generated ALWAYS AS IDENTITY, we assume they start at 1 and increment.
    existing_instances = []

    for i in range(1, NUM_INSTANCES + 1):
        layout_id = random.randint(1, len(course_layouts))
        num_studs = random.randint(15, 80)
        period_val = random.choice(valid_periods)  # Picking 1, 2, 3, 4, or 5
        year = '2024'

        # Note: In your schema, study_period_name IS the foreign key and part of PK
        f.write(
            f"INSERT INTO course_instance (study_period_name, num_students, study_year, course_layout_id) VALUES ({period_val}, {num_studs}, '{year}', {layout_id});\n")

        existing_instances.append({'id': i, 'period': period_val})

    # ---------------------------------------------------------
    # 4. PLANNED ACTIVITIES (Linking to Composite Key)
    # ---------------------------------------------------------
    f.write("\n-- Planned Activities\n")

    # We need to track exactly which activities exist to allocate people to them
    # Structure: List of tuples (course_instance_id, teaching_activity_id, study_period_name)
    existing_planned_activities = []

    for instance in existing_instances:
        # Create 1-3 activities per course instance
        num_activities = random.randint(1, 3)

        # Pick random activity types (Lecture=1, Lab=2 etc)
        chosen_types = random.sample(range(1, len(teaching_activities) + 1), num_activities)

        for act_type_id in chosen_types:
            hours = random.randint(10, 50)
            cid = instance['id']
            pid = instance['period']

            f.write(
                f"INSERT INTO planned_activity (course_instance_id, teaching_activity_id, study_period_name, planned_hours) VALUES ({cid}, {act_type_id}, {pid}, {hours});\n")

            existing_planned_activities.append((cid, act_type_id, pid))

    # ---------------------------------------------------------
    # 5. ALLOCATIONS (Linking to Planned Activity)
    # ---------------------------------------------------------
    f.write("\n-- Activity Allocations\n")

    for _ in range(NUM_INSTANCES * 2):  # Generate a bunch of allocations
        # Pick a valid planned activity
        if not existing_planned_activities:
            break

        (cid, act_id, pid) = random.choice(existing_planned_activities)
        emp_id = random.randint(1, NUM_PEOPLE)

        # Your table tracks Allocation ID (Identity), Employee, CourseInstance, Activity, Period
        # We use ON CONFLICT DO NOTHING in case we randomly pick the exact same combo twice (optional)

        f.write(
            f"INSERT INTO activity_allocation (employee_id, course_instance_id, teaching_activity_id, study_period_name) VALUES ({emp_id}, {cid}, {act_id}, {pid});\n")

    # ---------------------------------------------------------
    # 6. CLEANUP CIRCULAR DEPENDENCY
    # ---------------------------------------------------------
    f.write("\n-- Update Departments Manager\n")
    for dep_id in range(1, len(departments) + 1):
        mgr_id = random.randint(1, 5)
        f.write(f"UPDATE department SET manager_id = {mgr_id} WHERE department_id = {dep_id};\n")

print(f"Done! Created {FILENAME}")