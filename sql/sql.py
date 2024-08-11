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

reindex_newer_12 = '''
SELECT 1;
'''

reindex_older_12 = '''
SELECT 1;
'''

reindex_pk_older_12 = '''
-- Create the new index concurrently
{new_index_def_conc};

-- Trasaction mode
BEGIN;

-- Drop the constraint related to index
ALTER TABLE {table_name}
    DROP CONSTRAINT {index_name};

-- Recreate the index using the new index
ALTER TABLE {table_name}
    ADD CONSTRAINT {index_name}
        PRIMARY KEY using INDEX {new_index_def_conc};

COMMIT;

ALTER INDEX {new_index_def_conc} RENAME TO {index_name};
'''