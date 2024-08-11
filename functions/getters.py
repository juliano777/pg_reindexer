#_*_ encoding: utf-8 _*_

from distutils.version import LooseVersion

from sql.sql import get_index_info
from sql.sql import get_server_version
from sql.sql import reindex_newer_12
from sql.sql import reindex_older_12
from sql.sql import reindex_pk_older_12


def del_cursor(cur):
    cur.close()
    del cur

def pg_version(conn) -> str:
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(get_server_version)
    res = str(LooseVersion(cur.fetchone()[0]))
    del_cursor(cur)
    return res


def index_info(conn, schema_name: str, index_name: str) -> dict:
    # SQL
    sql = get_index_info.format(
                                schema_name=schema_name,
                                index_name=index_name)

    conn.autocommit = True
    cur = conn.cursor()

    # Execute the query
    cur.execute(sql)

    # Result
    res = cur.fetchone()

    del_cursor(cur)

    d = {
        'schema_name': schema_name,
        'index_name': index_name,
        'index_id': res[0],
        'table_id': res[1],
        'table_name': res[2],
        'is_unique': res[3],
        'is_primary': res[4],
        'index_def': res[5],
        'index_def_conc': None,
        'new_index_name': None,
        'new_index_def_conc': None,    
        }
    
    d['index_def_conc'] = d['index_def'].replace('INDEX', 'INDEX CONCURRENTLY')

    d['new_index_name'] = f"new_{d['index_name']}"
    
    d['new_index_def_conc'] = d['index_def_conc'].replace(
        d['index_name'],
        d['new_index_name']
        )

    return d

def get_version_newer_than_11(version: str) -> bool:
    return LooseVersion(version) > LooseVersion('11')

def get_reindex_sql(is_newer_than_11: bool, is_primary: bool):
    if is_newer_than_11:
        sql = reindex_newer_12
    elif is_primary:
        sql = reindex_pk_older_12
    else:
        sql = reindex_older_12
