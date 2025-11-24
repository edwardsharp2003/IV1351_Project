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
