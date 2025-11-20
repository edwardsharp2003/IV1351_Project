-- 1. Table for storing business rules (No changes needed here)
CREATE TABLE system_rules (
    rule_name VARCHAR(100) NOT NULL,
    rule_value INT NOT NULL
);

ALTER TABLE system_rules ADD CONSTRAINT PK_system_rules PRIMARY KEY (rule_name);

-- Insert the rule data (the number 4)
INSERT INTO system_rules (rule_name, rule_value)
VALUES ('max_courses_per_period', 4);


-- 2. The Corrected Trigger Function
CREATE OR REPLACE FUNCTION check_course_allocation_limit()
    RETURNS TRIGGER AS $$
DECLARE
    current_course_count INT;
    max_limit INT;
    target_period_id INT;
BEGIN
    -- A. Get the max limit (4) from system_rules
    SELECT rule_value INTO max_limit
    FROM system_rules
    WHERE rule_name = 'max_courses_per_period';

    -- B. Find the study_period_id from the new row being inserted/updated
    -- FIX: Changed 'study_period_name' to 'study_period_id' to match table schema
    target_period_id := NEW.study_period_id;

    -- C. Count courses employee is already teaching
    SELECT COUNT(DISTINCT aa.course_instance_id)
    INTO current_course_count
    FROM activity_allocation aa
    WHERE aa.employee_id = NEW.employee_id
      -- FIX: Use study_period_id for comparison
      AND aa.study_period_id = target_period_id
      -- This accounts for the new row being inserted/updated
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
-- NOTE: Changed to BEFORE INSERT OR UPDATE for robustness, matching standard business logic.
CREATE TRIGGER trg_check_allocation_limit
    BEFORE INSERT OR UPDATE ON activity_allocation
    FOR EACH ROW
EXECUTE FUNCTION check_course_allocation_limit();