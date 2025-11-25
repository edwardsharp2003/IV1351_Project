#!/bin/bash

# This script executes the query-1.sql file and then runs a SELECT
# statement on the 'planned_hours_per_course' view/table.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
DB_NAME="iv1351t2"

# Dynamically determine the script's directory to build robust relative paths.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
QUERY_FILE="$SCRIPT_DIR/../src/query-1.sql"


# --- Script ---

echo "--- Running Query 1 and follow-up SELECT ---"
echo ""

# 1. Verify that the referenced query file actually exists.
if [ ! -f "$QUERY_FILE" ]; then
    echo "Error: Query file not found at $QUERY_FILE" >&2
    exit 1
fi

# 2. Execute the main query from the .sql file.
echo "Running query from file: $QUERY_FILE"
psql -d "$DB_NAME" -f "$QUERY_FILE"

echo ""
echo "-----------------------------------------------"
echo "--- Verification Step ---"
echo ""

# 3. Execute the SELECT query against the view created by query-1.sql.
echo "Running: SELECT * FROM planned_hours_per_course;"
psql -d "$DB_NAME" -c "SELECT * FROM planned_hours_per_course;"

