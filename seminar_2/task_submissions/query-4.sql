CREATE OR REPLACE VIEW more_than_n_allocated AS
SELECT
    employee.employee_id AS "Employee ID",
    person.first_name || ' ' || person.last_name AS "Teacher's Name",
    activity_allocation.study_period_id AS "Period",
    COUNT(DISTINCT activity_allocation.course_instance_id) AS "Course Count"
FROM
    employee
JOIN
    person ON person.person_id = employee.person_id
JOIN
    activity_allocation ON activity_allocation.employee_id = employee.employee_id
WHERE
    activity_allocation.study_period_id = EXTRACT(QUARTER FROM CURRENT_DATE)
GROUP BY
    "Employee ID",
    "Teacher's Name",
    "Period"
HAVING
    COUNT(DISTINCT activity_allocation.course_instance_id) > 2 -- change to view at other course count
ORDER BY
    "Course Count" DESC;

SELECT * FROM more_than_n_allocated;