#_*_ encoding: utf-8 _*_

from functions.db_ops import pg_connect
from functions.getters import index_info as get_index_info
from functions.getters import pg_version as get_pgversion


# Connection string
dbconn = """
    host='localhost'
    port=5432
    dbname='postgres'
    user='postgres'
    password='123'
    application_name='foo'
"""

# Connect to Postgres
conn = pg_connect(dbconn)

# PostgreSQL version
pg_version = get_pgversion(conn)

# Just a test...
schema_name = 'public'
index_name = 'tournaments2_new_results_pkey'

# Index info (dict)
index_info = get_index_info(conn, 'public', 'tournaments2_new_results_pkey')

# Activate autocommit mode
# conn.autocommit = True

