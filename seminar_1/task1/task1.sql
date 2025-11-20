CREATE TABLE course_layout (
 course_layout_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 course_code    VARCHAR(10),
 course_name VARCHAR(500),
 min_students INT NOT NULL,
 max_students INT NOT NULL,
 hp DECIMAL(4,2),
 valid_from DATE
);

ALTER TABLE course_layout ADD CONSTRAINT PK_course_layout PRIMARY KEY (course_layout_id);


CREATE TABLE department (
 department_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 department_name  VARCHAR(100) NOT NULL,
 manager_id  INT
);

ALTER TABLE department ADD CONSTRAINT PK_department PRIMARY KEY (department_id);


CREATE TABLE employee (
 employee_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 person_id INT NOT NULL,
 job_title_id INT NOT NULL,
 department_id INT NOT NULL,
 manager_id INT NOT NULL,
 salary_history_id INT NOT NULL
);

ALTER TABLE employee ADD CONSTRAINT PK_employee PRIMARY KEY (employee_id);


CREATE TABLE job_title (
 job_title_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 job_title  VARCHAR(500) NOT NULL
);

ALTER TABLE job_title ADD CONSTRAINT PK_job_title PRIMARY KEY (job_title_id);


CREATE TABLE person (
 person_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 personal_number  CHAR(11) NOT NULL,
 first_name VARCHAR(500) NOT NULL,
 last_name VARCHAR(500) NOT NULL
);

ALTER TABLE person ADD CONSTRAINT PK_person PRIMARY KEY (person_id);


CREATE TABLE phone (
 person_id INT NOT NULL,
 phone_number VARCHAR(100) NOT NULL
);

ALTER TABLE phone ADD CONSTRAINT PK_phone PRIMARY KEY (person_id,phone_number);


CREATE TABLE salary_history (
 salary_history_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 salary_amount DECIMAL(10,2) NOT NULL,
 valid_from DATE NOT NULL,
 employee_id INT NOT NULL
);

ALTER TABLE salary_history ADD CONSTRAINT PK_salary_history PRIMARY KEY (salary_history_id);


CREATE TABLE skill (
 skill_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 skill_name VARCHAR(100) NOT NULL
);

ALTER TABLE skill ADD CONSTRAINT PK_skill PRIMARY KEY (skill_id);


CREATE TABLE study_period_type (
 study_period_id INT NOT NULL
);

ALTER TABLE study_period_type ADD CONSTRAINT PK_study_period_type PRIMARY KEY (study_period_id);


CREATE TABLE teaching_activity (
 teaching_activity_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 activity_name VARCHAR(500) NOT NULL,
 factor DECIMAL(4,2)
);

ALTER TABLE teaching_activity ADD CONSTRAINT PK_teaching_activity PRIMARY KEY (teaching_activity_id);


CREATE TABLE address (
 address_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 person_id INT NOT NULL,
 address VARCHAR(500) NOT NULL
);

ALTER TABLE address ADD CONSTRAINT PK_address PRIMARY KEY (address_id);


CREATE TABLE course_instance (
 course_instance_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 num_students INT NOT NULL,
 study_year VARCHAR(10),
 course_layout_id INT NOT NULL
);

ALTER TABLE course_instance ADD CONSTRAINT PK_course_instance PRIMARY KEY (course_instance_id);


CREATE TABLE course_instance_period (
 course_instance_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 study_period_id INT NOT NULL
);

ALTER TABLE course_instance_period ADD CONSTRAINT PK_course_instance_period PRIMARY KEY (course_instance_id,study_period_id);


CREATE TABLE employee_skill (
 employee_id INT NOT NULL,
 skill_id INT NOT NULL
);

ALTER TABLE employee_skill ADD CONSTRAINT PK_employee_skill PRIMARY KEY (employee_id,skill_id);


CREATE TABLE planned_activity (
 teaching_activity_id INT NOT NULL,
 course_instance_id INT NOT NULL,
 study_period_id INT NOT NULL,
 planned_hours INT NOT NULL
);

ALTER TABLE planned_activity ADD CONSTRAINT PK_planned_activity PRIMARY KEY (teaching_activity_id,course_instance_id,study_period_id);


CREATE TABLE activity_allocation  (
 activity_allocation_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
 employee_id INT NOT NULL,
 teaching_activity_id INT NOT NULL,
 course_instance_id INT NOT NULL,
 study_period_id INT NOT NULL
);

ALTER TABLE activity_allocation  ADD CONSTRAINT PK_activity_allocation  PRIMARY KEY (activity_allocation_id);


ALTER TABLE department ADD CONSTRAINT FK_department_0 FOREIGN KEY (manager_id ) REFERENCES employee (employee_id);


ALTER TABLE employee ADD CONSTRAINT FK_employee_0 FOREIGN KEY (person_id) REFERENCES person (person_id);
ALTER TABLE employee ADD CONSTRAINT FK_employee_1 FOREIGN KEY (job_title_id) REFERENCES job_title (job_title_id);
ALTER TABLE employee ADD CONSTRAINT FK_employee_2 FOREIGN KEY (department_id) REFERENCES department (department_id);
ALTER TABLE employee ADD CONSTRAINT FK_employee_3 FOREIGN KEY (manager_id) REFERENCES employee (employee_id);
ALTER TABLE employee ADD CONSTRAINT FK_employee_4 FOREIGN KEY (salary_history_id) REFERENCES salary_history (salary_history_id);


ALTER TABLE phone ADD CONSTRAINT FK_phone_0 FOREIGN KEY (person_id) REFERENCES person (person_id);


ALTER TABLE salary_history ADD CONSTRAINT FK_salary_history_0 FOREIGN KEY (employee_id) REFERENCES employee (employee_id);


ALTER TABLE address ADD CONSTRAINT FK_address_0 FOREIGN KEY (person_id) REFERENCES person (person_id);


ALTER TABLE course_instance ADD CONSTRAINT FK_course_instance_0 FOREIGN KEY (course_layout_id) REFERENCES course_layout (course_layout_id);


ALTER TABLE course_instance_period ADD CONSTRAINT FK_course_instance_period_0 FOREIGN KEY (course_instance_id) REFERENCES course_instance (course_instance_id);
ALTER TABLE course_instance_period ADD CONSTRAINT FK_course_instance_period_1 FOREIGN KEY (study_period_id) REFERENCES study_period_type (study_period_id);


ALTER TABLE employee_skill ADD CONSTRAINT FK_employee_skill_0 FOREIGN KEY (employee_id) REFERENCES employee (employee_id);
ALTER TABLE employee_skill ADD CONSTRAINT FK_employee_skill_1 FOREIGN KEY (skill_id) REFERENCES skill (skill_id);


ALTER TABLE planned_activity ADD CONSTRAINT FK_planned_activity_0 FOREIGN KEY (teaching_activity_id) REFERENCES teaching_activity (teaching_activity_id);
ALTER TABLE planned_activity ADD CONSTRAINT FK_planned_activity_1 FOREIGN KEY (course_instance_id,study_period_id) REFERENCES course_instance_period (course_instance_id,study_period_id);


ALTER TABLE activity_allocation  ADD CONSTRAINT FK_activity_allocation _0 FOREIGN KEY (employee_id) REFERENCES employee (employee_id);
ALTER TABLE activity_allocation  ADD CONSTRAINT FK_activity_allocation _1 FOREIGN KEY (teaching_activity_id,course_instance_id,study_period_id) REFERENCES planned_activity (teaching_activity_id,course_instance_id,study_period_id);


