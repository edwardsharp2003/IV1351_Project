/*
Calculate actual allocated hours for a course:
Calculate the total allocated hours with the multiplication factor along
with the break-ups for each activity and for each teacher, for a current years’ course instance.
Table 5 below is an example result of such a query, illustrating the expected output.

Course code | course instance id | HP | Teacher's Name | Designation | lecture H | tutorial H | lab H | seminar H | other overhead H | admin | exam | total H
 */

CREATE OR REPLACE VIEW planned_hours_per_teacher AS
SELECT
    cl.course_code AS "Course code",
    ci.course_instance_id AS "Course Instance ID",
    cl.HP AS "HP",
    p.first_name || ' ' || p.last_name AS "Teacher's name",
    jt.job_title AS "Designation"
FROM
    activity_allocation aa
JOIN
    planned_activity pa ON aa.teaching_activity_id = pa.teaching_activity_id AND
    aa.course_instance_id = pa.course_instance_id AND
    aa.study_period_id = pa.study_period_id
JOIN
    course_instance ci ON aa.course_instance_id = ci.course_instance_id
JOIN
    course_layout cl ON ci.course_layout_id = cl.course_layout_id
JOIN
    employee e ON aa.employee_id = e.employee_id
JOIN
    person p ON e.person_id = p.person_id
JOIN
    job_title jt ON e.job_title_id = jt.job_title_id
WHERE
    cl.course_code = 'CE101';

/*
SELECT * FROM planned_hours_per_teacher;
*/