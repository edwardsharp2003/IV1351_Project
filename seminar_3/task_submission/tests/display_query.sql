SELECT 
    ta.activity_name, 
    pa.teaching_activity_id,
    pa.planned_hours,
    aa.employee_id,
    pa.course_instance_id,
    pa.study_period_id
FROM planned_activity pa
JOIN activity_allocation aa 
  ON pa.teaching_activity_id = aa.teaching_activity_id 
  AND pa.course_instance_id = aa.course_instance_id
  AND pa.study_period_id = aa.study_period_id
JOIN teaching_activity ta   -- Join the third table here
  ON pa.teaching_activity_id = ta.teaching_activity_id
WHERE pa.teaching_activity_id = 9;