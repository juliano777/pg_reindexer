# Database operations

from sys import exit

from psycopg import connect

from functions.getters import index_info as get_index_info


# Function to connect to PostgreSQL
def pg_connect(dbconn: str):
    try:
        return connect(dbconn)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)


#


# Reindex (Postgres 11 or older)
def do_reindex(
    conn,
    schema_name: str,
    index_name: str,
    new_index_def_conc: str,
    table_name: str,
    index_name: str,
    new_index_def_conc    
    ) -> None:

    conn.autocommit = True
    cur = conn.cursor()

    sql = reindex_older12.format(
        table_name=table_name,
        index_name=index_name,
        new_index_def_conc=index_name,
        )
    
    cur.execute()
    del_cursor(cur)
