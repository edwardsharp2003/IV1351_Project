CREATE OR REPLACE VIEW hours_variance_report AS
WITH
-- Step 1: For every planned activity, calculate its hours and determine if it has been allocated.
-- We use a LEFT JOIN from planned_activity to activity_allocation. If a match is found, the activity is considered "allocated".
HoursBreakdown AS (
    SELECT
        pa.course_instance_id,
        (pa.planned_hours * ta.factor) AS activity_hours,
        -- If aa.employee_id is not null, the activity has been allocated. If null, it's unallocated.
        CASE
            WHEN aa.employee_id IS NOT NULL THEN (pa.planned_hours * ta.factor)
            ELSE 0
        END AS allocated_activity_hours
    FROM
        planned_activity pa
    JOIN
        teaching_activity ta ON pa.teaching_activity_id = ta.teaching_activity_id
    LEFT JOIN
        activity_allocation aa ON pa.teaching_activity_id = aa.teaching_activity_id
                               AND pa.course_instance_id = aa.course_instance_id
                               AND pa.study_period_id = aa.study_period_id
),
-- Step 2: Aggregate these hours for each course instance to get the totals.
AggregatedHours AS (
    SELECT
        course_instance_id,
        SUM(activity_hours) AS total_planned_hours,
        SUM(allocated_activity_hours) AS total_allocated_hours
    FROM
        HoursBreakdown
    GROUP BY
        course_instance_id
)
-- Step 3: Join to get course details, calculate the variance, and filter.
SELECT
    ah.course_instance_id,
    cl.course_code,
    ah.total_planned_hours,
    ah.total_allocated_hours,
    -- Calculate the variance as a percentage for readability. NULLIF prevents division by zero.
    TRUNC(
        (ABS(ah.total_planned_hours - ah.total_allocated_hours) / NULLIF(ah.total_planned_hours, 0) * 100),
        2
    ) AS "variance_percentage"
FROM
    AggregatedHours ah
JOIN
    course_instance ci ON ah.course_instance_id = ci.course_instance_id
JOIN
    course_layout cl ON ci.course_layout_id = cl.course_layout_id
WHERE
    -- Filter for course instances where the variance is greater than 15% (0.15).
    (ABS(ah.total_planned_hours - ah.total_allocated_hours) / NULLIF(ah.total_planned_hours, 0)) > 0.15;

-- You can now query this view to get the report.
SELECT * FROM hours_variance_report;