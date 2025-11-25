#!/bin/bash

# you might need to make the script executable by chmod +x create_db.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Dynamic path, makes it work no matter where the script is run from
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# The name of the database to be created.
DB_NAME="iv1351t2"

# The path to the Python script that generates the data.
PYTHON_SCRIPT="$SCRIPT_DIR/../src/data_generation.py"

# The path to the SQL script that sets up the database schema (tables, views, etc.).
SETUP_SQL="$SCRIPT_DIR/../src/task2.sql"

# Path to check allocation sql
CHECK_ALLOCATION_SQL="$SCRIPT_DIR/../src/check_allocation_limit.sql"

# The path to the SQL script that inserts the generated data.
DATA_SQL="$SCRIPT_DIR/../src/insert_data.sql"

# --- Script ---

echo "--- Starting Database Setup ---"

# 1. Drop the database if it exists, then create it.
echo "Re-creating database: $DB_NAME..."
dropdb --if-exists "$DB_NAME"
createdb "$DB_NAME"
echo "Database '$DB_NAME' created successfully."

# 2. Run the Python script to generate data.
echo "Running Python script to generate data: $PYTHON_SCRIPT..."
python3 "$PYTHON_SCRIPT"
echo "Data generation complete."

# 3. Run the setup SQL script.
echo "Running setup script: $SETUP_SQL..."
psql -d "$DB_NAME" -f "$SETUP_SQL"
echo "Setup script executed successfully."
psql -d "$DB_NAME" -f "$CHECK_ALLOCATION_SQL"
echo "Business rules sql executed successfully."

# 4. Insert the generated data into the database.
echo "Inserting data from: $DATA_SQL..."
psql -d "$DB_NAME" -f "$DATA_SQL"
echo "Data insertion complete."

echo "--- Database setup finished successfully! ---"
