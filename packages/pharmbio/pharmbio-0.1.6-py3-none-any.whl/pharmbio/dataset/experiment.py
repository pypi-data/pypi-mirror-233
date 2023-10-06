import polars as pl
from ..config import DB_URI, DATABASE_SCHEMA
from ..database.queries import experiment_name_sql_query


def get_projects_list(lookup: str = None):
    """
    Retrieves a list of projects.

    Args:
        lookup (str, optional): A string to filter the project list. Defaults to None.

    Returns:
        list: A list of project names.

    Example:
        ```python
        project_list = get_projects_list()
        print(project_list)
        # Output: ['Project A', 'Project B', 'Project C']

        filtered_list = get_projects_list(lookup='a')
        print(filtered_list)
        # Output: ['Project A']
        ```
    """

    query = experiment_name_sql_query(
        DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"],
        DATABASE_SCHEMA["EXPERIMENT_METADATA_TABLE_NAME_ON_DB"],
    )
    project_list = pl.read_database(query, DB_URI).to_dict(as_series=False)[
        DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"]
    ]

    project_list = list(filter(None, project_list))
    if lookup is not None:
        lookup = lookup.lower()
        project_list = [s for s in project_list if lookup in s.lower()]
    return project_list
