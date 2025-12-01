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
    COUNT(DISTINCT activity_allocation.course_instance_id) > 2 -- change to view at other max courses
ORDER BY
    "Course Count" DESC;

SELECT * FROM more_than_n_allocated;

/*
CREATE INDEX idx_activity_allocation_study_period_id ON activity_allocation (study_period_id);

    Your view has the WHERE activity_allocation.study_period_id = EXTRACT(QUARTER FROM CURRENT_DATE) clause. Without an index,
    the database must perform a "Sequential Scan" on the activity_allocation table, meaning it reads every single row to find
    the ones matching the current quarter. This index allows the database to directly and very quickly locate only the relevant rows,
    which is significantly more efficient.

CREATE INDEX idx_activity_allocation_employee_id ON activity_allocation (employee_id);

    Your view joins activity_allocation to employee on the employee_id column. After filtering the activity_allocation table,
    the database needs to find the matching employee records. This index acts like a quick lookup table, helping the database
    find the corresponding employee for each activity_allocation without having to search through the employee table. This speeds up the JOIN operation.

CREATE INDEX idx_employee_person_id ON employee (person_id);

    Similarly, your view joins employee to person on the person_id column. This index helps the database efficiently find
    the matching person record for each employee involved in the query.

  ---
  Note on Primary Keys:

  Your other join columns, employee.employee_id and person.person_id, are very likely PRIMARY KEYs. Primary keys in PostgreSQL are automatically indexed, so you almost certainly do not need to create
  indices on them. The indices listed above are for the other columns involved in filtering and joining.
*/

