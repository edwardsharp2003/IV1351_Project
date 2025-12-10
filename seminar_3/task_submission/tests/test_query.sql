-- ALTER course_instance (course_instance_id, num_students, study_year, course_layout_id)
-- VALUES (501, 100, 2025, 1);

UPDATE course_instance
SET num_students = num_students + 100
WHERE course_instance_id = 501;

UPDATE course_instance SET num_students = num_students - 100 WHERE course_instance_id = 501;