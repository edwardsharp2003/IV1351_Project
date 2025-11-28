#!/bin/bash

# You might need to make the script executable by running: chmod +x query-2.sh

# Exit immediately if a command exits with a non-zero status.
set -e

DB_NAME="iv1351t2"

# Dynamic path, makes it work no matter where the script is run from
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Define path to SQL file relative to script
SQL_FILE="$SCRIPT_DIR/../src/query-2.sql"

echo "--- Running Query 2 Script ---"

# 1. Update the view definition from the SQL file.
echo "Creating/replacing view 'planned_hours_per_teacher'..."

# Prompt for the year to filter the view
echo -n "Please enter the year to filter the view (e.g., 2024): "
read year_filter

# Validate that the year is a 4-digit number
if ! [[ "$year_filter" =~ ^[0-9]{4}$ ]]; then
  echo "Error: Please enter a valid 4-digit year."
  exit 1
fi

# Execute query-2.sql, passing the year as a psql variable to filter the view
psql -d "$DB_NAME" -v year_filter="'$year_filter'" -f "$SQL_FILE"

# Check if the last command succeeded.
if [ $? -ne 0 ]; then
  echo "Error: Failed to create or replace the view. Please check your SQL file. Aborting."
  exit 1
fi
echo "View updated successfully for year $year_filter."
echo ""

# 2. Prompt the user for the course code to query the filtered view.
echo -n "Please enter the course code to query (e.g., DD2350): "
read course_code

# Validate that the input is not empty
if [ -z "$course_code" ]; then
  echo "Error: Course code cannot be empty."
  exit 1
fi

# 3. Define and execute the final SELECT query on the year-filtered view.
echo ""
echo "Fetching results for course code '$course_code' in year $year_filter..."

# Pass the user input to psql as a variable and query the view
psql -d "$DB_NAME" -v code_filter="'$course_code'" <<EOF
SELECT * FROM planned_hours_per_teacher WHERE "Course code" = :code_filter ORDER BY "Teacher's name";
EOF

echo "--- Done ---"
