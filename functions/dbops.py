# Database operations

from sys import exit

from psycopg import connect

# Function to connect to PostgreSQL
def pg_connect(dbconn: str):
    try:
        return connect(dbconn)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
