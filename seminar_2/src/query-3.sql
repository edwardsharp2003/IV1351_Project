/*
Calculate the total allocated hours (with multiplication factors) for a teacher,
only for the current years’ course instances.
*/

CREATE OR REPLACE VIEW teacher_hours_per_course_instance AS
SELECT
    cl.course_code AS "Course code",
    ci.course_instance_id AS "Course Instance ID",
    cl.HP AS "HP",
    cip.study_period_id AS "Period",
    p.first_name || ' ' || p.last_name AS "Teacher's Name",
    -- Hours per teaching activity
    COALESCE(SUM(CASE
        WHEN ta.activity_name = 'Lecture'
            THEN pa.planned_hours * ta.factor
        END), 0) AS "Lecture Hours",
    COALESCE(SUM(CASE
        WHEN ta.activity_name = 'Tutorial'
            THEN pa.planned_hours * ta.factor
        END), 0) AS "Tutorial Hours",
    COALESCE(SUM(CASE
        WHEN ta.activity_name = 'Lab'
            THEN pa.planned_hours * ta.factor
        END), 0) AS "Lab Hours",
    COALESCE(SUM(CASE
        WHEN ta.activity_name = 'Seminar'
            THEN pa.planned_hours * ta.factor
        END), 0) AS "Seminar Hours",
    COALESCE(SUM(CASE
        WHEN ta.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar')
            THEN pa.planned_hours * ta.factor
        END), 0) AS "Other Overhead Hours",
    -- Admin and Exam hours (Note: These are calculated per course, not per teacher, and will appear the same for all teachers on the same course instance)
    (2 * cl.hp + 28 + 0.2 * ci.num_students) AS "Admin Hours",
    (32 + 0.725 * ci.num_students) AS "Exam Hours",
    -- Total hours calculation
    (
    COALESCE(SUM(pa.planned_hours * ta.factor), 0) +
        (2 * cl.hp + 28 + 0.2 * ci.num_students) +
        (32 + 0.725 * ci.num_students)
    ) AS "Total Hours"
FROM
    activity_allocation aa
JOIN
    planned_activity pa ON aa.teaching_activity_id = pa.teaching_activity_id AND
                         aa.course_instance_id = pa.course_instance_id AND
                         aa.study_period_id = pa.study_period_id
JOIN
    course_instance ci ON aa.course_instance_id = ci.course_instance_id
JOIN
    course_instance_period cip ON ci.course_instance_id = cip.course_instance_id
JOIN
    course_layout cl ON ci.course_layout_id = cl.course_layout_id
JOIN
    employee e ON aa.employee_id = e.employee_id
JOIN
    person p ON e.person_id = p.person_id
JOIN
    teaching_activity ta ON pa.teaching_activity_id = ta.teaching_activity_id
WHERE
    ci.study_year = :year_filter AND e.employee_id = :teacher_id_filter -- Using variables for the year and teacher ID
GROUP BY
    cl.course_code,
    ci.course_instance_id,
    cl.HP,
    cip.study_period_id,
    "Teacher's Name",
    ci.num_students;

-- SELECT * FROM teacher_hours_per_course_instance;
-- psql -d iv1351t2 -v year_filter="'2025'" -f seminar_2/src/query-3.sql