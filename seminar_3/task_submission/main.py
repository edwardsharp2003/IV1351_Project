import os
import sys
import psycopg
from dotenv import load_dotenv

from src.dao import SchoolDAO
from src.controller import Controller
from src.view import Cli


def main():
    """
    Main entry point for the application.
    Initializes and wires all components together.
    """
    load_dotenv()

    try:
        conn = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME")
        )
        # Ensure autocommit is off for transactional control, as per the assignment.
        conn.autocommit = False

        # Create instances of the application layers
        dao = SchoolDAO(conn)
        controller = Controller(dao)
        cli = Cli(controller)

        # Start the application
        cli.start()

    except psycopg.OperationalError as e:
        print(f"Database connection error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error has occurred: {e}", file=sys.stderr)
    finally:
        if 'conn' in locals() and conn:
            conn.close()


if __name__ == "__main__":
    main()
