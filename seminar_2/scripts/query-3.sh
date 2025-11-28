#!/bin/bash

# You might need to make the script executable by running: chmod +x query-3.sh

# Exit immediately if a command exits with a non-zero status.
set -e

DB_NAME="iv1351t2"

# Dynamic path, makes it work no matter where the script is run from
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SQL_FILE="$SCRIPT_DIR/../src/query-3.sql"

echo "--- Running Query 3 Script ---"

# 1. Prompt for the year
echo -n "Please enter the year to query (e.g., 2024): "
read year_filter

if ! [[ "$year_filter" =~ ^[0-9]{4}$ ]]; then
  echo "Error: Please enter a valid 4-digit year."
  exit 1
fi

# 2. Prompt for the teacher's employee_id
echo -n "Please enter the teacher's employee ID to query: "
read teacher_id

if ! [[ "$teacher_id" =~ ^[0-9]+$ ]]; then
  echo "Error: Please enter a valid number for the employee ID."
  exit 1
fi

# 3. Re-create the view with the specified filters
echo ""
echo "Generating report for teacher ID #$teacher_id in year $year_filter..."
psql -d "$DB_NAME" -v year_filter="'$year_filter'" -v teacher_id_filter="$teacher_id" -f "$SQL_FILE"

# 4. Display the results from the view
psql -d "$DB_NAME" -c "SELECT * FROM teacher_hours_per_course_instance;"

echo "--- Done ---"
