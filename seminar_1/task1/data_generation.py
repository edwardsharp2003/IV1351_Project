import random
from faker import Faker

# Initialize Faker
fake = Faker()

# CONFIGURATION
NUM_PEOPLE = 50
NUM_COURSES = 10
NUM_INSTANCES = 20 # Total course instances
FILENAME = "insert_data.sql"

def escape_sql(text):
    """Helper to handle O'Connor and other names with quotes"""
    return text.replace("'", "''")

print(f"Generating data into {FILENAME}...")

with open(FILENAME, "w") as f:
    f.write("-- Generated Data Script\n")
    
    # ---------------------------------------------------------
    # 1. STATIC DICTIONARIES (Civil Eng / IT Context)
    # ---------------------------------------------------------
    departments = ["Civil Engineering", "Information Technology", "Architecture", "Urban Planning"]
    job_titles = ["Lecturer", "Senior Lecturer", "Professor", "PhD Student", "Administrator"]
    skills = ["Python", "SQL", "AutoCAD", "Revit", "GIS", "Project Management", "Matlab"]
    teaching_activities = [("Lecture", 1.0), ("Lab", 2.0), ("Seminar", 1.5), ("Project Supervision", 0.5)]
    
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
        ("CE500", "Master Thesis Project")
    ]

    # ---------------------------------------------------------
    # 2. INSERT INDEPENDENT TABLES
    # ---------------------------------------------------------
    
    # Departments (Manager ID is NULL initially to avoid circular dependency error)
    f.write("\n-- Departments\n")
    for dept in departments:
        f.write(f"INSERT INTO department (department_name, manager_id) VALUES ('{dept}', NULL);\n")

    # Job Titles
    f.write("\n-- Job Titles\n")
    for job in job_titles:
        f.write(f"INSERT INTO job_title (job_title) VALUES ('{job}');\n")

    # Skills
    f.write("\n-- Skills\n")
    for skill in skills:
        f.write(f"INSERT INTO skill (skill_name) VALUES ('{skill}');\n")

    # Teaching Activities
    f.write("\n-- Teaching Activities\n")
    for name, factor in teaching_activities:
        f.write(f"INSERT INTO teaching_activity (activity_name, factor) VALUES ('{name}', {factor});\n")

    # Course Layouts
    f.write("\n-- Course Layouts\n")
    for code, name in course_layouts:
        hp = random.choice([7.5, 15.0, 3.0])
        min_s = random.randint(10, 20)
        max_s = random.randint(30, 100)
        f.write(f"INSERT INTO course_layout (course_code, course_name, min_students, max_students, hp) VALUES ('{code}', '{name}', {min_s}, {max_s}, {hp});\n")

    # ---------------------------------------------------------
    # 3. PEOPLE & EMPLOYEES
    # ---------------------------------------------------------
    f.write("\n-- People, Addresses, Phones, Employees\n")
    
    # We track generated IDs (Postgres generates them sequentially 1..N)
    employee_ids = []
    
    for i in range(1, NUM_PEOPLE + 1):
        # Person
        sex = random.choice(['M', 'F'])
        if sex == 'M':
            fn = fake.first_name_male()
            ln = fake.last_name_male()
        else:
            fn = fake.first_name_female()
            ln = fake.last_name_female()
            
        # Fake Swedish personal number
        p_num = f"{random.randint(1970, 2003)}{random.randint(10,12)}{random.randint(10,28)}-{random.randint(1000,9999)}"
        
        f.write(f"INSERT INTO person (personal_number, first_name, last_name) VALUES ('{p_num}', '{escape_sql(fn)}', '{escape_sql(ln)}');\n")
        
        # Address & Phone (Linked to person_id = i)
        addr = escape_sql(fake.address().replace("\n", ", "))
        phone = fake.phone_number()
        f.write(f"INSERT INTO address (person_id, address) VALUES ({i}, '{addr}');\n")
        f.write(f"INSERT INTO phone (person_id, phone_number) VALUES ({i}, '{phone}');\n")

        # Employee
        salary = random.randint(30000, 65000)
        dept_id = random.randint(1, len(departments))
        job_id = random.randint(1, len(job_titles))
        
        # Logic for manager: The first 5 people have no manager, others report to 1-5
        manager_id = "NULL"
        if i > 5:
            manager_id = random.randint(1, 5)

        f.write(f"INSERT INTO employee (salary, person_id, job_title_id, department_id, manager_id) VALUES ({salary}, {i}, {job_id}, {dept_id}, {manager_id});\n")
        employee_ids.append(i)

    # ---------------------------------------------------------
    # 4. COURSE INSTANCES & ALLOCATIONS
    # ---------------------------------------------------------
    f.write("\n-- Course Instances\n")
    
    # Generate instances
    for i in range(1, NUM_INSTANCES + 1):
        layout_id = random.randint(1, len(course_layouts))
        num_students = random.randint(15, 80)
        period = random.choice(['P1', 'P2', 'P3', 'P4'])
        year = '2024'
        
        f.write(f"INSERT INTO course_instance (course_layout_id, num_students, study_period, study_year) VALUES ({layout_id}, {num_students}, '{period}', '{year}');\n")

    f.write("\n-- Planned Activities & Allocations\n")
    
    # For each course instance, create 1-3 activities and assign a random teacher
    allocation_counter = 0
    
    for instance_id in range(1, NUM_INSTANCES + 1):
        # Create 2 activities per course (e.g., one lecture, one lab)
        for _ in range(2):
            act_id = random.randint(1, len(teaching_activities))
            hours = random.randint(10, 40)
            
            # Insert Planned Activity
            # Note: Since PK is (course_instance_id, teaching_activity_id), 
            # we need to be careful not to insert duplicates. 
            # For simplicity in this script, we assume specific ID combinations.
            # To be safe, we will perform an "ON CONFLICT DO NOTHING" in a real scenario, 
            # but for this simple generator, we will skip duplicate logic validation 
            # and trust the loop won't collide often or let SQL handle errors.
            # A better strategy:
            
            f.write(f"INSERT INTO planned_activity (course_instance_id, teaching_activity_id, planned_hours) VALUES ({instance_id}, {act_id}, {hours}) ON CONFLICT DO NOTHING;\n")

            # Allocate an Employee
            # We pick a random employee (ID 1 to NUM_PEOPLE)
            emp_id = random.randint(1, NUM_PEOPLE)
            
            # Constraint Check Logic:
            # Your trigger checks max 4 courses per period.
            # Since we are generating random data, we might accidentally hit this.
            # We will just write the INSERT statement. If it fails due to the trigger,
            # the SQL script will show an error for that line but continue if we run it right.
            
            f.write(f"INSERT INTO activity_allocation (employee_id, course_instance_id, teaching_activity_id) VALUES ({emp_id}, {instance_id}, {act_id}) ON CONFLICT DO NOTHING;\n")

    # ---------------------------------------------------------
    # 5. CLEANUP CIRCULAR DEPENDENCIES
    # ---------------------------------------------------------
    f.write("\n-- Update Departments with Managers\n")
    # Assign random employees (1-5) as managers for the departments
    for dep_id in range(1, len(departments) + 1):
        mgr_id = random.randint(1, 5) 
        f.write(f"UPDATE department SET manager_id = {mgr_id} WHERE department_id = {dep_id};\n")

print(f"Done! SQL file '{FILENAME}' created.")
