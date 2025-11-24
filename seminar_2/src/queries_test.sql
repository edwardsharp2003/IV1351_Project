-- seminar_2/src/queries_test.sql

-- Query 1: Planned hours calculations
-- Calculate the total hours (with the multiplication factor) along with the break-ups for each activity,
-- for the current years’ course instances.

CREATE OR REPLACE VIEW planned_hours_per_course AS
SELECT
    cl.course_code,
    ci.course_instance_id,
    cl.hp,
    cip.study_period_id AS period,
    ci.num_students,
    -- Calculate planned hours for each activity type, applying the factor
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Lecture' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS lecture_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Tutorial' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS tutorial_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Lab' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS lab_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Seminar' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS seminar_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar') THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS other_overhead_hours,
    -- Calculate derived admin and exam hours
    (2 * cl.hp + 28 + 0.2 * ci.num_students) AS admin_hours,
    (32 + 0.725 * ci.num_students) AS exam_hours,
    -- Calculate total hours
    (
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Lecture' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Tutorial' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Lab' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Seminar' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar') THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        (2 * cl.hp + 28 + 0.2 * ci.num_students) +
        (32 + 0.725 * ci.num_students)
    ) AS total_hours
FROM
    course_instance ci
JOIN
    course_layout cl ON ci.course_layout_id = cl.course_layout_id
JOIN
    course_instance_period cip ON ci.course_instance_id = cip.course_instance_id
JOIN
    planned_activity pa ON ci.course_instance_id = pa.course_instance_id AND cip.study_period_id = pa.study_period_id
JOIN
    teaching_activity ta ON pa.teaching_activity_id = ta.teaching_activity_id
WHERE
    ci.study_year = '2024' -- Assuming '2024' is the current year
GROUP BY
    cl.course_code,
    ci.course_instance_id,
    cl.hp,
    cip.study_period_id,
    ci.num_students
ORDER BY
    ci.course_instance_id;

-- To run this query:
-- SELECT * FROM planned_hours_per_course;

-- Expected Output for Query 1: (Please run the query in your psql client and paste the output here for reporting)
/*
<PASTE QUERY 1 OUTPUT HERE>
*/


-- Query 2: Actual allocated hours for a course
-- Calculate the total allocated hours with the multiplication factor along with the break-ups for each activity and for each teacher, for a current years’ course instance.

CREATE OR REPLACE VIEW allocated_hours_per_course_and_teacher AS
SELECT
    cl.course_code,
    ci.course_instance_id,
    cl.hp,
    p.first_name || ' ' || p.last_name AS teacher_name,
    jt.job_title AS designation,
    -- Allocated hours for each activity type, applying the factor
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Lecture' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS lecture_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Tutorial' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS tutorial_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Lab' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS lab_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Seminar' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS seminar_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar') THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS other_overhead_hours,
    -- Derived admin and exam hours are per course instance, needs to be distributed per teacher or handled differently.
    -- For simplicity, assuming these are also 'allocated' if a teacher is allocated to *any* activity in the course.
    -- This might need clarification based on exact business rules for allocation of Admin/Exam hours.
    (2 * cl.hp + 28 + 0.2 * ci.num_students) AS admin_hours,
    (32 + 0.725 * ci.num_students) AS exam_hours,
    (
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Lecture' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Tutorial' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Lab' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Seminar' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar') THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        (2 * cl.hp + 28 + 0.2 * ci.num_students) +
        (32 + 0.725 * ci.num_students)
    ) AS total_allocated_hours
FROM
    activity_allocation aa
JOIN
    employee e ON aa.employee_id = e.employee_id
JOIN
    person p ON e.person_id = p.person_id
JOIN
    job_title jt ON e.job_title_id = jt.job_title_id
JOIN
    planned_activity pa ON aa.teaching_activity_id = pa.teaching_activity_id
                        AND aa.course_instance_id = pa.course_instance_id
                        AND aa.study_period_id = pa.study_period_id
JOIN
    teaching_activity ta ON pa.teaching_activity_id = ta.teaching_activity_id
JOIN
    course_instance ci ON aa.course_instance_id = ci.course_instance_id
JOIN
    course_layout cl ON ci.course_layout_id = cl.course_layout_id
WHERE
    ci.study_year = '2024'
GROUP BY
    cl.course_code,
    ci.course_instance_id,
    cl.hp,
    p.first_name,
    p.last_name,
    jt.job_title,
    ci.num_students
ORDER BY
    ci.course_instance_id, teacher_name;

-- To run this query:
-- SELECT * FROM allocated_hours_per_course_and_teacher;

-- Expected Output for Query 2: (Please run the query in your psql client and paste the output here for reporting)
/*
<PASTE QUERY 2 OUTPUT HERE>
*/


-- Query 3: Total allocated hours for a teacher
-- Calculate the total allocated hours (with multiplication factors) for a teacher, only for the current years’ course instances.

CREATE OR REPLACE VIEW total_allocated_hours_per_teacher AS
SELECT
    p.first_name || ' ' || p.last_name AS teacher_name,
    e.employee_id,
    cl.course_code,
    ci.course_instance_id,
    cl.hp,
    cip.study_period_id AS period,
    -- Allocated hours for each activity type, applying the factor
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Lecture' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS lecture_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Tutorial' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS tutorial_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Lab' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS lab_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name = 'Seminar' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS seminar_hours,
    COALESCE(SUM(CASE WHEN ta.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar') THEN pa.planned_hours * ta.factor ELSE 0 END), 0) AS other_overhead_hours,
    -- Derived admin and exam hours are per course instance, needs to be distributed per teacher or handled differently.
    -- For simplicity, summing these up per teacher, implicitly assuming full allocation for these by any activity allocation.
    SUM(2 * cl.hp + 28 + 0.2 * ci.num_students) AS admin_hours,
    SUM(32 + 0.725 * ci.num_students) AS exam_hours,
    (
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Lecture' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Tutorial' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Lab' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name = 'Seminar' THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        COALESCE(SUM(CASE WHEN ta.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar') THEN pa.planned_hours * ta.factor ELSE 0 END), 0) +
        SUM(2 * cl.hp + 28 + 0.2 * ci.num_students) +
        SUM(32 + 0.725 * ci.num_students)
    ) AS total_allocated_hours
FROM
    activity_allocation aa
JOIN
    employee e ON aa.employee_id = e.employee_id
JOIN
    person p ON e.person_id = p.person_id
JOIN
    planned_activity pa ON aa.teaching_activity_id = pa.teaching_activity_id
                        AND aa.course_instance_id = pa.course_instance_id
                        AND aa.study_period_id = pa.study_period_id
JOIN
    teaching_activity ta ON pa.teaching_activity_id = ta.teaching_activity_id
JOIN
    course_instance ci ON aa.course_instance_id = ci.course_instance_id
JOIN
    course_layout cl ON ci.course_layout_id = cl.course_layout_id
JOIN
    course_instance_period cip ON ci.course_instance_id = cip.course_instance_id AND aa.study_period_id = cip.study_period_id
WHERE
    ci.study_year = '2024'
GROUP BY
    p.first_name,
    p.last_name,
    e.employee_id,
    cl.course_code,
    ci.course_instance_id,
    cl.hp,
    cip.study_period_id
ORDER BY
    teacher_name, ci.course_instance_id;

-- To run this query:
-- SELECT * FROM total_allocated_hours_per_teacher;

-- Expected Output for Query 3: (Please run the query in your psql client and paste the output here for reporting)
/*
<PASTE QUERY 3 OUTPUT HERE>
*/


-- Query 4: Teachers allocated to more than a specific number of course instances
-- List employee ids and names of all teachers who are allocated in more than a specific number of course instances during the current period.

CREATE OR REPLACE VIEW teachers_exceeding_course_limit AS
SELECT
    e.employee_id,
    p.first_name || ' ' || p.last_name AS teacher_name,
    aa.study_period_id AS period,
    COUNT(DISTINCT aa.course_instance_id) AS num_courses_allocated
FROM
    activity_allocation aa
JOIN
    employee e ON aa.employee_id = e.employee_id
JOIN
    person p ON e.person_id = p.person_id
WHERE
    -- Assuming 'current period' means any period in the current year, and we're checking per period.
    -- The trigger checks per period, so this query should also reflect that.
    -- We can filter by a specific year if needed, but the prompt implies 'current period' is sufficient.
    TRUE
GROUP BY
    e.employee_id,
    p.first_name,
    p.last_name,
    aa.study_period_id
HAVING
    COUNT(DISTINCT aa.course_instance_id) > (SELECT rule_value FROM system_rules WHERE rule_name = 'max_courses_per_period')
ORDER BY
    num_courses_allocated DESC, teacher_name;

-- To run this query:
-- SELECT * FROM teachers_exceeding_course_limit;

-- Expected Output for Query 4: (Please run the query in your psql client and paste the output here for reporting)
/*
<PASTE QUERY 4 OUTPUT HERE>
*/


-- EXPLAIN ANALYZE for Query 1: Planned hours calculations
-- This will show the execution plan and actual runtime statistics for the view.
-- To use, you would run this command in your psql client.

EXPLAIN ANALYZE SELECT * FROM planned_hours_per_course;

-- Expected EXPLAIN ANALYZE Output for Query 1: (Please run the query in your psql client and paste the output here for reporting)
/*
<PASTE EXPLAIN ANALYZE OUTPUT HERE>
*/
