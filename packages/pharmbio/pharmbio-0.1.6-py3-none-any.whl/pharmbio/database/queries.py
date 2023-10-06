from .. import config as cfg


def experiment_name_sql_query(experiment_name, table_name_on_db):
    """
    Executes a SQL query to retrieve experiment names from a specified table.

    Args:
        experiment_name (str): The name of the experiment column to select.
        table_name_on_db (str): The name of the table to query.

    Returns:
        str: The SQL query string.

    Example:
        ```python
        experiment_name = 'experiment_name'
        table_name_on_db = 'experiment_table'

        query = experiment_name_sql_query(experiment_name, table_name_on_db)
        print(query)
        ```
    """
    return f"""
            SELECT {experiment_name}
            FROM {table_name_on_db}
            GROUP BY {experiment_name}
            ORDER BY {experiment_name}
            """


def experiment_metadata_sql_query(name, db_schema, experiment_type):
    """
    Executes a SQL query to retrieve experiment metadata from the database.

    Args:
        name (str): The name of the experiment to search for.
        db_schema (dict): A dictionary containing the names of the database schema tables.
        experiment_type (str): The type of experiment to filter by.

    Returns:
        str: The SQL query string.

    Example:
        ```python
        name = 'my_experiment'
        db_schema = {
            'EXPERIMENT_METADATA_TABLE_NAME_ON_DB': 'experiment_table',
            'EXPERIMENT_NAME_COLUMN': 'name',
            'EXPERIMENT_ANALYSIS_DATE_COLUMN': 'analysis_date',
            'EXPERIMENT_PLATE_BARCODE_COLUMN': 'plate_barcode',
            'EXPERIMENT_PLATE_ACQID_COLUMN': 'plate_acqid',
            'EXPERIMENT_ANALYSIS_ID_COLUMN': 'analysis_id'
        }
        experiment_type = 'cp-features'

        query = experiment_metadata_sql_query(name, db_schema, experiment_type)
        print(query)
        ```
    """
    return f"""
            SELECT *
            FROM {db_schema['EXPERIMENT_METADATA_TABLE_NAME_ON_DB']}
            WHERE {db_schema['EXPERIMENT_NAME_COLUMN']} LIKE '%%{name}%%'
            AND meta->>'type' = '{experiment_type}'
            AND {db_schema['EXPERIMENT_ANALYSIS_DATE_COLUMN']} IS NOT NULL
            ORDER BY {db_schema['EXPERIMENT_PLATE_BARCODE_COLUMN']}, {db_schema['EXPERIMENT_PLATE_ACQID_COLUMN']}, {db_schema['EXPERIMENT_ANALYSIS_ID_COLUMN']}
            """


def plate_layout_sql_query(db_schema, plate_barcode):
    """
    Executes a SQL query to retrieve plate layout information from the database.

    Args:
        db_schema (dict): A dictionary containing the names of the database schema tables.
        plate_barcode (str): The barcode of the plate to query.

    Returns:
        str: The SQL query string.

    Example:
        ```python
        db_schema = {
            'PLATE_LAYOUT_TABLE_NAME_ON_DB': 'plate_v1',
            'PLATE_LAYOUT_BARCODE_COLUMN': 'barcode',
            'PLATE_COMPOUND_NAME_COLUMN': 'batch_id'
        }
        plate_barcode = 'ABC123'

        query = plate_layout_sql_query(db_schema, plate_barcode)
        print(query)
        ```
    """
    return f"""
            SELECT {', '.join(cfg.PLATE_LAYOUT_INFO)}
            FROM {db_schema['PLATE_LAYOUT_TABLE_NAME_ON_DB']}
            WHERE ({db_schema['PLATE_LAYOUT_BARCODE_COLUMN']} IN ({plate_barcode}))
            AND {db_schema['PLATE_COMPOUND_NAME_COLUMN']} <> ''
            """
