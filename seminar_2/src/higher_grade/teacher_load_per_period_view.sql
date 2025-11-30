CREATE OR REPLACE VIEW  teacher_load_per_period_view
AS
SELECT
    e.employee_id,
    p.first_name,
    p.last_name,
    ci.study_year,
    cip.study_period_id,
    SUM(pa.planned_hours * ta.factor) AS teacher_load
FROM
    employee e
JOIN
    person p ON e.person_id = p.person_id
JOIN
    activity_allocation aa ON e.employee_id = aa.employee_id
JOIN
    planned_activity pa ON aa.teaching_activity_id = pa.teaching_activity_id
                        AND aa.course_instance_id = pa.course_instance_id
                        AND aa.study_period_id = pa.study_period_id
JOIN
    teaching_activity ta ON pa.teaching_activity_id = ta.teaching_activity_id
JOIN
    course_instance ci ON pa.course_instance_id = ci.course_instance_id
JOIN
    course_instance_period cip ON ci.course_instance_id = cip.course_instance_id
                                AND pa.study_period_id = cip.study_period_id
GROUP BY
    e.employee_id,
    p.first_name,
    p.last_name,
    ci.study_year,
    cip.study_period_id

-- To refresh the materialized view, run the following command:
-- REFRESH MATERIALIZED VIEW teacher_load_per_period_mv;
