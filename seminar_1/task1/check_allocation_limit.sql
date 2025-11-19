-- 1. Table for storing business rules (No changes needed here)
CREATE TABLE system_rules (
    rule_name VARCHAR(100) NOT NULL,
    rule_value INT NOT NULL
);

ALTER TABLE system_rules ADD CONSTRAINT PK_system_rules PRIMARY KEY (rule_name);

-- Insert the rule data (the number 4)
INSERT INTO system_rules (rule_name, rule_value)
VALUES ('max_courses_per_period', 4);


-- 2. The Updated Trigger Function
CREATE OR REPLACE FUNCTION check_course_allocation_limit()
    RETURNS TRIGGER AS $$
DECLARE
    current_course_count INT;
    max_limit INT;
    target_period_id INT; -- Changed from VARCHAR to INT
BEGIN
    -- A. Get the max limit (4) from system_rules
    SELECT rule_value INTO max_limit
    FROM system_rules
    WHERE rule_name = 'max_courses_per_period';

    -- B. Find the study_period
    -- OPTIMIZATION: In your new schema, 'study_period_name' is already inside
    -- the activity_allocation table (NEW row). We don't need to look it up!
    target_period_id := NEW.study_period_name;

    -- C. Count courses employee is already teaching
    -- OPTIMIZATION: No need to JOIN course_instance anymore.
    SELECT COUNT(DISTINCT aa.course_instance_id)
    INTO current_course_count
    FROM activity_allocation aa
    WHERE aa.employee_id = NEW.employee_id
      AND aa.study_period_name = target_period_id
      -- Don't count the course we are currently trying to add
      AND aa.course_instance_id != NEW.course_instance_id;

    -- D. Check if limit is reached
    IF current_course_count >= max_limit THEN
        RAISE EXCEPTION 'Employee (ID: %) is already allocated to % courses in Period ID %.',
            NEW.employee_id, max_limit, target_period_id;
    END IF;

    -- If the check passes, allow the INSERT/UPDATE
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- 3. Attach trigger to table
CREATE TRIGGER trg_check_allocation_limit
    BEFORE INSERT ON activity_allocation
    FOR EACH ROW
EXECUTE FUNCTION check_course_allocation_limit();