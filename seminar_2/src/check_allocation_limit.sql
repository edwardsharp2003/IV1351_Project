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
BEGIN
    -- Get the max limit from system_rules
    SELECT rule_value INTO max_limit FROM system_rules WHERE rule_name = 'max_courses_per_period';

    -- Count distinct course instances for the employee in the target period
    SELECT COUNT(DISTINCT course_instance_id)
    INTO current_course_count
    FROM activity_allocation
    WHERE employee_id = NEW.employee_id
      AND study_period_id = NEW.study_period_id;

    -- Check if the new allocation would exceed the limit
    IF TG_OP = 'INSERT' AND current_course_count >= max_limit THEN
        RAISE EXCEPTION 'Employee (ID: %) cannot be allocated to more than % courses in Period ID %.',
            NEW.employee_id, max_limit, NEW.study_period_id;
    END IF;

    -- For updates, the logic is more complex. If the employee or period changes, it's like a new allocation.
    -- This simplified version just re-checks, but a more robust solution might be needed.
    IF TG_OP = 'UPDATE' AND (NEW.employee_id != OLD.employee_id OR NEW.study_period_id != OLD.study_period_id) THEN
        SELECT COUNT(DISTINCT course_instance_id)
        INTO current_course_count
        FROM activity_allocation
        WHERE employee_id = NEW.employee_id
          AND study_period_id = NEW.study_period_id;

        IF current_course_count >= max_limit THEN
            RAISE EXCEPTION 'Employee (ID: %) cannot be allocated to more than % courses in Period ID %.',
                NEW.employee_id, max_limit, NEW.study_period_id;
        END IF;
    END IF;


    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- 3. Attach trigger to table
-- NOTE: Changed to BEFORE INSERT OR UPDATE for robustness, matching standard business logic.
CREATE TRIGGER trg_check_allocation_limit
    BEFORE INSERT OR UPDATE ON activity_allocation
    FOR EACH ROW
EXECUTE FUNCTION check_course_allocation_limit();