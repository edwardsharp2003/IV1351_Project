DROP MATERIALIZED VIEW IF EXISTS teacher_load_per_period_mv;

CREATE MATERIALIZED VIEW teacher_load_per_period_mv AS
SELECT
    cip.study_period_id AS "Period",
    ci.study_year AS "Year",
    p.first_name || ' ' || p.last_name AS "Teacher's Name",
    -- Hours per teaching activity (aggregated across all courses in the period)
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
    -- Admin and Exam hours (summed across all courses in the period)
    SUM(2 * cl.hp + 28 + 0.2 * ci.num_students) AS "Admin Hours",
    SUM(32 + 0.725 * ci.num_students) AS "Exam Hours",
    -- Total hours calculation
    (
        COALESCE(SUM(pa.planned_hours * ta.factor), 0) +
        SUM(2 * cl.hp + 28 + 0.2 * ci.num_students) +
        SUM(32 + 0.725 * ci.num_students)
    ) AS "Total Hours"
FROM
    activity_allocation aa
JOIN
    planned_activity pa ON aa.teaching_activity_id = pa.teaching_activity_id
                        AND aa.course_instance_id = pa.course_instance_id
                        AND aa.study_period_id = pa.study_period_id
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
    CAST(ci.study_year AS INTEGER) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY
    cip.study_period_id,
    ci.study_year,
    p.first_name,
    p.last_name
ORDER BY
    "Teacher's Name",
    cip.study_period_id
WITH DATA;

-- Query the materialized view
SELECT * FROM teacher_load_per_period_mv;

