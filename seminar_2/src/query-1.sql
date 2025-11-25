/*
Planned hours calculations: Calculate the total hours (with the multiplication factor)
along with the break-ups for each activity, for the current years’ course instances.

Table output:
Course code | course instance id | HP | period | #students | lecture H | tutorial H | lab H | seminar H | other overhead H | admin | exam | total H
*/

CREATE OR REPLACE VIEW planned_hours_per_course AS
SELECT
    course_layout.course_code,
    course_instance.course_instance_id,
    course_layout.HP,
    course_instance_period.study_period_id,
    course_instance.num_students,
    --- Hours per teaching activity
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Lecture'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) AS lecture_hours,
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Tutorial'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) AS tutorial_hours,
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Lab'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) AS lab_hours,
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Seminar'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) AS seminar_hours,
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar')
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) AS other_overhead_hours,
    (2 * course_layout.hp + 28 + 0.2 * course_instance.num_students) AS admin_hours,
    (32 + 0.725 * course_instance.num_students) AS exam_hours,
    --- Total hours calculation
    (
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Lecture'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) +
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Tutorial'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) +
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Lab'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) +
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name = 'Seminar'
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) +
    COALESCE(SUM(CASE
        WHEN teaching_activity.activity_name NOT IN ('Lecture', 'Tutorial', 'Lab', 'Seminar')
            THEN planned_activity.planned_hours * teaching_activity.factor
        ELSE 0 END), 0) +
    (2 * course_layout.hp + 28 + 0.2 * course_instance.num_students) +
    (32 + 0.725 * course_instance.num_students)
    ) AS total_hours
FROM
    course_instance
JOIN
    course_layout ON course_instance.course_layout_id = course_layout.course_layout_id
JOIN
    course_instance_period ON course_instance.course_instance_id = course_instance_period.course_instance_id
JOIN
    planned_activity ON course_instance_period.course_instance_id = planned_activity.course_instance_id AND course_instance_period.study_period_id = planned_activity.study_period_id
JOIN
    teaching_activity ON planned_activity.teaching_activity_id = teaching_activity.teaching_activity_id
WHERE
    course_instance.study_year = '2024' -- Assuming '2024' is the current year
GROUP BY
    course_layout.course_code,
    course_instance.course_instance_id,
    course_layout.hp,
    course_instance_period.study_period_id,
    course_instance.num_students
ORDER BY
    course_instance.course_instance_id;

-- To run this query:
-- SELECT * FROM planned_hours_per_course;