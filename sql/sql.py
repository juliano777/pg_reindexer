get_index_info = """
SELECT
    i.indexrelid AS index_id,
    ct.oid AS table_id,
    ct.relname AS table_name,
    i.indisunique AS is_unique,
    i.indisprimary AS is_primary,
    pg_get_indexdef(i.indexrelid) AS index_def
FROM pg_index i
INNER JOIN pg_class AS ci
    ON ci.oid = i.indexrelid
INNER JOIN pg_namespace AS n
    ON n.oid = ci.relnamespace
INNER JOIN pg_class AS ct
    ON ct.oid = i.indrelid
WHERE n.nspname = '{schema_name}'
    AND ci.relname = '{index_name}';
"""

get_server_version = """
SELECT
    split_part(setting, ' ', 1)
FROM pg_settings
WHERE name = 'server_version'
"""
