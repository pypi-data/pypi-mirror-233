import os
import glob
import polars as pl
from typing import Union, List, Dict
from .. import config as cfg
from ..config import DATABASE_SCHEMA

from ..logger import (
    log_info,
    log_warning,
)

from ..database.queries import (
    experiment_metadata_sql_query,
)

from ..utils import (
    get_file_extension,
    read_file,
)


def _get_image_quality_refrence_df(experiment_name: str):
    """
    Gets an image quality reference dataframe and associated data dictionary from the database for a given experiment name.

    Returns a dataframe containing image quality metadata and plate barcodes for the given experiment, and a dictionary mapping experiment names to lists of plate barcodes.

    Args:
    experiment_name: The name of the experiment to retrieve data for

    Returns:
    image_quality_reference_df: A dataframe containing image quality metadata
    data_dict: A dictionary mapping experiment names to lists of plate barcodes
    """

    query = experiment_metadata_sql_query(
        experiment_name, DATABASE_SCHEMA, cfg.IMAHGE_QUALITY_METADATA_TYPE
    )
    image_quality_reference_df = pl.read_database(query, cfg.DB_URI)
    data_dict = (
        image_quality_reference_df.select(
            [
                DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"],
                DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"],
            ]
        )
        .groupby(DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"])
        .agg(pl.col(DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]))
        .to_dicts()
    )
    return image_quality_reference_df, data_dict


def _logging_information_image_quality_ref(
    image_quality_reference_df: pl.DataFrame,
    image_quality_data_dict: Dict,
    experiment_name: str,
    unique_project_count: int,
):
    """
    Logs information about the given image quality reference dataframe, data dictionary, and experiment name.

    Logs a message indicating the number of studies found for the given experiment name. Logs the data dictionary mapping experiments to plate barcodes. Logs any replicated analyses found in the dataframe.

    Args:
    image_quality_reference_df: A dataframe containing image quality metadata
    image_quality_data_dict: A dictionary mapping experiment names to lists of plate barcodes
    experiment_name: The name of the experiment queried
    unique_project_count: The number of unique studies found for the experiment
    """

    if unique_project_count == 0:
        message = f"Quering the db for {experiment_name} returned nothing."
    elif unique_project_count > 1:
        message = (
            f"Quering the db for {experiment_name} found {unique_project_count} studies: "
            f"{image_quality_reference_df.unique(DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN'])[DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN']].to_list()}"
        )
    else:
        message = (
            f"Quering the db for {experiment_name} found {unique_project_count} study: "
            f"{image_quality_reference_df.unique(DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN'])[DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN']].to_list()}"
        )
    log_info(f"{message}\n{'_'*50}")

    if unique_project_count != 0:
        for i, study in enumerate(image_quality_data_dict, start=1):
            log_info(i)
            for value in study.values():
                log_info("\t" + str(value))
    log_info("\n" + "_" * 50)

    grouped_replicates = image_quality_reference_df.groupby(
        DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]
    )

    for plate_name, group in grouped_replicates:
        if len(group) > 1:
            log_warning(
                (
                    f"Analysis for the plate with barcode {plate_name} is replicated {len(group)} times with "
                    f"{DATABASE_SCHEMA['EXPERIMENT_ANALYSIS_ID_COLUMN']} of {sorted(group[DATABASE_SCHEMA['EXPERIMENT_ANALYSIS_ID_COLUMN']].to_list())}"
                )
            )
    if image_quality_reference_df.filter(
        pl.col(DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]).is_duplicated()
    ).is_empty():
        log_info("No replicated analysis has been found!")


def get_image_quality_ref(
    name: str,
    drop_replication: Union[str, List[int]] = "Auto",
    keep_replication: Union[str, List[int]] = "None",
    filter: dict = None,
):
    """
    Retrieves the image quality reference data from the database based on the provided name and optional filters.

    Args:
        name (str): The name of experiment for the image quality reference.
        drop_replication (Union[str, List[int]], optional): The replication(s) to drop. Default is set to "Auto" which keep the experiment with highest id number (latest experiment). It can be "None" or a list of analysis_id.
        keep_replication (Union[str, List[int]], optional): The replication(s) to keep. Defaults to "None".
        filter (dict, optional): Filters to apply to the data. Defaults to None.

    Returns:
        polars.DataFrame: The image quality reference data.

    Examples:
        ```python
        name = "example"
        drop_replication = [1, 2]
        keep_replication = "None"
        filter = {"column1": ["value1", "value2"], "column2": ["value3"]}

        result = get_image_quality_ref(name, drop_replication, keep_replication, filter)
        ```
    """

    image_quality_reference, data_dict = _get_image_quality_refrence_df(name)
    unique_project_count = image_quality_reference.unique(
        DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"]
    ).height

    _logging_information_image_quality_ref(
        image_quality_reference, data_dict, name, unique_project_count
    )

    if drop_replication == "Auto" and keep_replication == "None":
        # keeping the highest analysis_id value of replicated rows
        image_quality_reference = (
            image_quality_reference.sort(
                DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"], descending=True
            )
            .unique(DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"], keep="first")
            .sort(DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"])
        )
    elif isinstance(drop_replication, list):
        # drop rows by analysis_id
        image_quality_reference = image_quality_reference.filter(
            ~pl.col(DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"]).is_in(
                drop_replication
            )
        )
    elif isinstance(keep_replication, list):
        # keep rows by analysis_id
        image_quality_reference = image_quality_reference.filter(
            pl.col(DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"]).is_in(
                keep_replication
            )
        )

    if filter is None:
        return image_quality_reference

    conditions = []
    for key, values in filter.items():
        # Create an OR condition for each value associated with a key
        key_conditions = [pl.col(key).str.contains(val) for val in values]
        combined_key_condition = key_conditions[0]
        for condition in key_conditions[1:]:
            combined_key_condition = combined_key_condition | condition
        conditions.append(combined_key_condition)
    # Combine all conditions with AND
    final_condition = conditions[0]
    for condition in conditions[1:]:
        final_condition = final_condition & condition
    # Apply the condition to the DataFrame
    return image_quality_reference.filter(final_condition)


def get_image_quality_data(
    filtered_image_quality_info: pl.DataFrame,
    force_merging_columns: Union[bool, str] = False,
):
    """
    Retrieves and processes image quality data based on the provided filtered image quality information.

    Args:
        filtered_image_quality_info (polars.DataFrame): The filtered image quality information.
        force_merging_columns (Union[bool, str], optional): Specifies how to handle merging columns. Defaults to False. 'keep' will keep all columns and fill missing values with null, 'drop' will merge dfs horizontally, only keeps matching columns, False will return None.

    Returns:
        polars.DataFrame: The concatenated and processed image quality data.

    Examples:
        ```python
        filtered_image_quality_ref = get_image_quality_ref()
        force_merging_columns = "keep"

        result = get_image_quality_data(filtered_image_quality_ref, force_merging_columns)
        ```
    """

    # Read and process all the files in a list, skipping files not found
    dfs = []
    for row in filtered_image_quality_info.iter_rows(named=True):
        file_path_name_schemes = [
            # Original naming scheme (file path + file prefix + plate barcode)
            row[DATABASE_SCHEMA["EXPERIMENT_RESULT_DIRECTORY_COLUMN"]]
            + cfg.IMAGE_QUALITY_FILE_PREFIX
            + "_"
            + row[DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]],
            # Alternative naming scheme without plate barcode (file path + file prefix)
            row[DATABASE_SCHEMA["EXPERIMENT_RESULT_DIRECTORY_COLUMN"]]
            + cfg.IMAGE_QUALITY_FILE_PREFIX,
        ]

        for file_path_name_scheme in file_path_name_schemes:
            if ext := get_file_extension(file_path_name_scheme):
                image_quality_data_file = file_path_name_scheme
                df = read_file(image_quality_data_file, ext)
                # Cast all numerical f64 columns to f32
                for name, dtype in zip(df.columns, df.dtypes):
                    if dtype == pl.Float64:
                        df = df.with_columns(pl.col(name).cast(pl.Float32))
                    elif dtype == pl.Int64:
                        df = df.with_columns(pl.col(name).cast(pl.Int32))
                dfs.append(df)
                log_info(
                    f"Successfully imported {df.shape}: {image_quality_data_file}{ext}"
                )
                break
        else:
            log_warning(f"No image quality file was found in: {file_path_name_schemes}")

    if force_merging_columns == "keep":
        concat_method = "diagonal"  # keep all columns and fill missing values with null
    elif force_merging_columns == "drop":
        concat_method = (
            "vertical"  # merge dfs horizontally, only keeps matching columns
        )
        common_columns = set(dfs[0].columns)
        for df in dfs[1:]:
            common_columns.intersection_update(df.columns)
        dfs = [df.select(sorted(common_columns)) for df in dfs]
    else:
        # Check if all dataframes have the same shape, if not print a message
        if len({df.shape[1] for df in dfs}) > 1:
            log_warning(
                "\nDataframes have different shapes and cannot be stacked together!"
            )
            return None
        concat_method = "vertical"  # standard vertical concatenation

    log_info(f"\n{'_'*50}\nQuality control data of {len(dfs)} plates imported!\n")

    sorting_column_map = [
        cfg.IMAGE_ID_COLUMN_NAME,
        cfg.METADATA_ACQID_COLUMN,
        cfg.METADATA_BARCODE_COLUMN,
        cfg.METADATA_WELL_COLUMN,
        cfg.METADATA_SITE_COLUMN,
        cfg.METADATA_IMAGE_NUMBER_COLUMN,
    ]
    # Concatenate all the dataframes at once and return it
    return (
        pl.concat(dfs, how=concat_method)
        .with_columns(cfg.CONSTRUCTING_IMAGE_ID)
        .sort(cfg.IMAGE_ID_COLUMN_NAME)
        .select(
            pl.col(sorting_column_map),
            pl.exclude(sorting_column_map),
        )
        if dfs
        else None
    )
