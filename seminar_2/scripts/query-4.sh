#!/bin/bash

# you might need to make the script executable by chmod +x query-4.sh

DB_NAME="iv1351t2"

# Dynamic path, makes it work no matter where the script is run from
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Define path to SQL file relative to script
SQL_FILE="$SCRIPT_DIR/../src/query-4.sql"

# Update VIEW
psql -d "$DB_NAME" -f "$SQL_FILE"

# Check if the last command succeeded. If not, exit the script.
if [ $? -ne 0 ]; then
  echo "Error: Failed to create or replace the view. Please check your SQL file. Aborting."
  exit 1
fi

# Prompt the user for input
echo "Please enter the study period ID to query: "
read study_period_id

# Validate that the input is a number between 1-4
if ! [[ "$study_period_id" =~ ^[0-9]+$ ]]; then
  echo "Error: The input must be a valid number."
  exit 1
elif (( study_period_id < 1 || study_period_id > 4 )); then
  echo "Error: Please enter a valid number between 1 and 4."
  exit 1
fi

# Define and execute the final SELECT query.
echo ""
echo "Fetching results for period $study_period_id..."

psql -d "$DB_NAME" -v period_id="$study_period_id" <<EOF
SELECT * FROM teacher_course_allocation WHERE study_period_id = :period_id ORDER BY teacher_name;
EOF