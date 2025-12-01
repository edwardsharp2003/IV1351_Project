CREATE INDEX idx_aa_period_employee ON activity_allocation (study_period_id, employee_id);

/*
This is a composite index that directly supports the two main filters and the grouping used in the query.

The WHERE clause filters on study_period_id. The GROUP BY and the rest of the query heavily use employee_id.
By placing them together, the database can rapidly find all relevant rows for the current period and group
them without hitting the actual table data (if it can perform an index-only scan).
*/

CREATE INDEX idx_employee_person_id ON employee (person_id);

/*
These are standard optimizations for the JOIN operations used in the query (activity_allocation to employee, and employee to person).
*/

