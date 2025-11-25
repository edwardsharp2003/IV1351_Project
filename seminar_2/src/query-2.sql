/*
Calculate actual allocated hours for a course:
Calculate the total allocated hours with the multiplication factor along
with the break-ups for each activity and for each teacher, for a current years’ course instance.
Table 5 below is an example result of such a query, illustrating the expected output.

Course code | course instance id | HP | Teacher's Name | Designation | lecture H | tutorial H | lab H | seminar H | other overhead H | admin | exam | total H
 */

CREATE OR REPLACE VIEW planned_hours_per_teacher AS
SELECT
    course_layout.course_code,
    course_instance.course_instance_id,
    course_layout.HP,
    person.first_name || ' ' || person.last_name AS "Teacher's name",
    job_title.job_title AS Designation
FROM
    course_instance
JOIN
    course_layout ON course_instance.course_layout_id = course_layout.course_layout_id
JOIN
    course_instance_period ON course_instance.course_instance_id = course_instance_period.course_instance_id
JOIN
    planned_activity ON course_instance_period.course_instance_id = planned_activity.course_instance_id AND
    course_instance_period.study_period_id = planned_activity.study_period_id
JOIN
    activity_allocation ON planned_activity.teaching_activity_id = activity_allocation.teaching_activity_id AND
    planned_activity.course_instance_id = activity_allocation.course_instance_id AND
    planned_activity.study_period_id = activity_allocation.study_period_id
JOIN
    employee ON activity_allocation.employee_id = employee.employee_id
JOIN
    person ON employee.person_id = person.person_id
JOIN
    job_title ON employee.job_title_id = job_title.job_title_id

ORDER BY
    course_layout.course_code,
    course_instance.course_instance_id,
    "Teacher's name";

/*
SELECT * FROM planned_hours_per_teacher;
*/