/*
List employee ids and names of all teachers who are allocated in more than a specific
number of course instances during the current period.
Table 7 below is an example result of such a query, illustrating the expected output.

employee_id | teachers_name | period | number of courses
*/


CREATE OR REPLACE VIEW teacher_course_allocation AS
SELECT
    employee.employee_id,
    person.first_name || ' ' || person.last_name AS teacher_name,
    activity_allocation.study_period_id,
    COUNT(DISTINCT activity_allocation.course_instance_id) AS course_count
FROM
    employee
JOIN
    person ON person.person_id = employee.person_id
JOIN
    activity_allocation ON activity_allocation.employee_id = employee.employee_id
GROUP BY
    employee.employee_id,
    teacher_name,
    activity_allocation.study_period_id;

--- to see view:
SELECT * FROM teacher_course_allocation WHERE study_period_id = 3;

