#_*_ encoding: utf-8 _*_

from distutils.version import LooseVersion

from sql.sql import get_index_info
from sql.sql import get_server_version

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
        'index_id': res[0],
        'table_id': res[1],
        'table_name': res[2],
        'is_unique': res[3],
        'is_primary': res[4],
        'index_name_temp': f'{index_name}_temp',
        'index_def': res[5],
        }

    index_def_conc = d['index_def'].replace('INDEX', 'INDEX CONCURRENTLY')

    temp_index_def_conc = index_def_conc.replace(
        index_name,
        d['index_name_temp']
    )

    d.update(
        {
            'index_def_conc': index_def_conc,
            'temp_index_def_conc': temp_index_def_conc,
         },

        )

    return d

def get_version_newer_than_11(version: str) -> bool:
    return LooseVersion(version) > LooseVersion('11')