import os
import re
import polars as pl
import pandas as pd
import polars.selectors as cs
from pathlib import Path
from typing import Union, Optional, List, Dict
from tqdm.notebook import tqdm
from .. import config as cfg
from ..utils import has_gpu
from ..data_processing import feature_aggregation as fa
from ..database.queries import (
    experiment_metadata_sql_query,
    plate_layout_sql_query,
)
from ..logger import (
    log_info,
    log_warning,
)


def get_cell_morphology_ref(
    name: str,
    filter: Optional[Dict[str, str]] = None,
):
    """
    Retrieves cell morphology references from the database based on the specified name and optional filter to select desired rows.

    Args:
        name (str): The name of the cell morphology reference.
        filter (dict, optional): A dictionary specifying the filter conditions. Each key represents a column name, and the corresponding value is a list of values to match. Defaults to None.

    Returns:
        pl.DataFrame: The filtered cell morphology references DataFrame.

    Example:
        ```python
        name = "example_reference"
        filter = {
            "column1": ["value_1", "value2"],  # values are combined with OR, and key-values are combined with AND
            "column2": ["value3"]
        }
        filtered_df = get_cell_morphology_ref(name, filter)
        display(filtered_df)
        ```
    """

    query = experiment_metadata_sql_query(
        name,
        cfg.DATABASE_SCHEMA,
        cfg.CELL_MORPHOLOGY_METADATA_TYPE,
    )
    df = pl.read_database(query, cfg.DB_URI)

    if filter is None:
        return df
    conditions = []
    # Iterate over each key-value pair in the filter dictionary
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
    return df.filter(final_condition)


def _get_join_columns(object_type: str) -> list:
    """Generates a list of columns to join on based on the object type.

    Parameters:
        object_type (str): The type of the object, must be one of 'cells', 'cytoplasm', 'nuclei'.

    Returns:
        list: A list of columns to join on.

    Raises:
        ValueError: If the object_type is not one of the allowed types.
    """

    # Extract allowed types dynamically from cfg.OBJECT_FILE_NAMES
    allowed_types = {name.split("_")[-1] for name in cfg.OBJECT_FILE_NAMES}

    if object_type not in allowed_types:
        raise ValueError(
            f"Invalid object_type. Allowed types are: {', '.join(allowed_types)}"
        )

    base_columns = [
        cfg.METADATA_ACQID_COLUMN,
        cfg.METADATA_BARCODE_COLUMN,
        cfg.METADATA_WELL_COLUMN,
        cfg.METADATA_SITE_COLUMN,
    ]

    join_columns = [f"{col}_{object_type}" for col in base_columns]

    specific_column_key = (
        cfg.OBJECT_ID_COLUMN
        if object_type == "cells"
        else cfg.OBJECT_PARENT_CELL_COLUMN
    )
    specific_column = f"{specific_column_key}_{object_type}"

    return join_columns + [specific_column]


def _join_object_dataframes(dfs: Dict[str, pl.DataFrame]) -> pl.DataFrame:
    """Merges multiple object-related dataframes based on specified columns.

    Parameters:
        dfs (Dict[str, pl.DataFrame]): Dictionary containing dataframes keyed by object type ('cells', 'cytoplasm', 'nuclei').

    Returns:
        pl.DataFrame: The joined dataframe.
    """
    log_info("Merging the data")
    # Join nuclei and cell data on specified columns
    combined_df = dfs["cells"].join(
        dfs["nuclei"],
        left_on=_get_join_columns("cells"),
        right_on=_get_join_columns("nuclei"),
        how="left",
        suffix="_nuclei",
    )

    # Further join with cytoplasm data on specified columns and return it
    return combined_df.join(
        dfs["cytoplasm"],
        left_on=_get_join_columns("cells"),
        right_on=_get_join_columns("cytoplasm"),
        how="left",
        suffix="_cytoplasm",
    )


def _rename_joined_df_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Renames specific columns in the dataframe by removing the last part after the last underscore or '_cells' that was attached during joining dfs.

    Parameters:
        df (pl.DataFrame): The original joined dataframe with columns to rename.

    Returns:
        pl.DataFrame: The dataframe with renamed columns.
    """
    specific_columns = [
        cfg.METADATA_ACQID_COLUMN,
        cfg.METADATA_BARCODE_COLUMN,
        cfg.METADATA_WELL_COLUMN,
        cfg.METADATA_SITE_COLUMN,
        cfg.CELL_CYTOPLASM_COUNT_COLUMN,
        cfg.CELL_NUCLEI_COUNT_COLUMN,
    ]

    rename_map = {f"{col}_cells": col for col in specific_columns}

    return df.rename(rename_map)


def _add_image_cell_id_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Adds unique Image ID and Cell ID columns to the dataframe by concatenating existing metadata columns.

    Parameters:
        df (pl.DataFrame): The original dataframe.

    Returns:
        pl.DataFrame: The dataframe with added columns.
    """
    # Create ImageID column by concatenating other columns
    image_id = (
        df[cfg.METADATA_ACQID_COLUMN]
        + "_"
        + df[cfg.METADATA_BARCODE_COLUMN]
        + "_"
        + df[cfg.METADATA_WELL_COLUMN]
        + "_"
        + df[cfg.METADATA_SITE_COLUMN]
    ).alias("image_id")

    df = df.with_columns([image_id])

    # Create CellID column by adding ImageID and cell object number
    cell_id = (df["image_id"] + "_" + df[f"{cfg.OBJECT_ID_COLUMN}_cells"]).alias(
        "cell_id"
    )

    return df.with_columns([cell_id])


def _drop_unwanted_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Drops specified columns if they exist in the dataframe.

    Parameters:
        df (pl.DataFrame): The original dataframe.

    Returns:
        pl.DataFrame: The dataframe with specified columns dropped.
    """
    # List of columns to drop
    drop_map = [
        "Children_cytoplasm_Count_nuclei",
        "Parent_precells_cells",
        "Parent_nuclei_cytoplasm",
        "Parent_cells_unfiltered_cells",  # exist in some of the experiment
        "Parent_nuclei_unfiltered_nuclei",  # exist in some of the experiment
        "Parent_cytoplasm_unfiltered_cytoplasm",  # exist in some of the experiment
        "ObjectNumber_cells",
        "ObjectNumber_nuclei",
        "ObjectNumber_cytoplasm",
    ]

    # Drop columns that exist in the list and the dataframe
    return df.drop([col for col in drop_map if col in df.columns])


def _cast_metadata_type_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Ensures data type consistency for specified metadata columns.

    Parameters:
        df (pl.DataFrame): The original dataframe.

    Returns:
        pl.DataFrame: The dataframe with specified columns cast to the correct data type.
    """
    # Define metadata columns to cast
    metadata_columns = [
        cfg.METADATA_ACQID_COLUMN,
        cfg.METADATA_BARCODE_COLUMN,
        cfg.METADATA_WELL_COLUMN,
        cfg.METADATA_SITE_COLUMN,
    ]

    # Cast each metadata column to the desired data type using list comprehension
    cast_cols = [pl.col(column).cast(pl.Utf8) for column in metadata_columns]

    return df.with_columns(cast_cols)


def _get_morphology_feature_cols(df: pl.DataFrame) -> List:
    """Returnd the columns in the dataframe that are morphology features.

    Parameters:
        df (pl.DataFrame): The original dataframe.

    Returns:
        pl.DataFrame: The dataframe with reordered columns.
    """
    morphology_feature_cols_list = df.select(cs.by_dtype(pl.NUMERIC_DTYPES)).columns
    morphology_feature_cols_list.remove(cfg.CELL_NUCLEI_COUNT_COLUMN)
    morphology_feature_cols_list.remove(cfg.CELL_CYTOPLASM_COUNT_COLUMN)
    return morphology_feature_cols_list


def _reorder_dataframe_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Reorders the columns in the dataframe based on data types and specific columns.

    Parameters:
        df (pl.DataFrame): The original dataframe.

    Returns:
        pl.DataFrame: The dataframe with reordered columns.
    """
    morphology_feature_cols = _get_morphology_feature_cols(df)
    non_numeric_cols = df.select(cs.by_dtype(pl.Utf8)).columns
    new_order = (
        sorted(non_numeric_cols)
        + [
            cfg.CELL_NUCLEI_COUNT_COLUMN,
            cfg.CELL_CYTOPLASM_COUNT_COLUMN,
        ]
        + morphology_feature_cols
    )

    return df.select(new_order)


def _merge_with_plate_info(df: pl.DataFrame) -> pl.DataFrame:
    """Merges the object dataframe with plate information.

    Parameters:
        df (pl.DataFrame): The object dataframe containing cellular morphology features.
        plate_layout_sql_query (callable): A function that returns SQL query for fetching plate layout info.

    Returns:
        pl.DataFrame: Dataframe with merged plate information.
    """

    # Extract unique barcodes
    barcode_list = df[cfg.METADATA_BARCODE_COLUMN].unique().to_list()
    barcode_str = ", ".join([f"'{item}'" for item in barcode_list])

    # Fetch plate layout data from db
    query = plate_layout_sql_query(cfg.DATABASE_SCHEMA, barcode_str)
    df_plates = pl.read_database(query, cfg.DB_URI)

    # Merge dataframes
    df = df.join(
        df_plates,
        how="left",
        left_on=[
            cfg.METADATA_BARCODE_COLUMN,
            cfg.METADATA_WELL_COLUMN,
        ],
        right_on=[
            cfg.DATABASE_SCHEMA["PLATE_LAYOUT_BARCODE_COLUMN"],
            cfg.DATABASE_SCHEMA["PLATE_LAYOUT_WELL_COLUMN"],
        ],
    )

    return df.drop_nulls(subset=cfg.DATABASE_SCHEMA["PLATE_COMPOUND_NAME_COLUMN"])


def get_cell_morphology_data(
    cell_morphology_ref_df: Union[pl.DataFrame, pd.DataFrame],
    aggregation_level: str = "cell",
    aggregation_method: Optional[Dict[str, str]] = None,
    path_to_save: str = "data",
    use_gpu: bool = False,
    save_plate_separately: bool = False,
):
    """
    Retrieves cell morphology data from the specified cell morphology reference DataFrame and performs aggregation at the specified level.

    Args:
        cell_morphology_ref_df (Union[pl.DataFrame, pd.DataFrame]): The cell morphology reference DataFrame.
        aggregation_level (str, optional): The level at which to perform aggregation. Defaults to "cell". It can be one of the following: "cell", "site", "well", "plate", "compound".
        aggregation_method (Dict[str, str], optional): The aggregation method for each level. Defaults to None.
        You shoul set the aggregation method for each level in a dictionary. Possible values are: "mean", "median", "sum", "min", "max", "first", "last".
        path_to_save (str, optional): The path to save the aggregated data. Defaults to "data".
        use_gpu (bool, optional): Whether to use GPU acceleration. Defaults to False.

    Returns:
        pl.DataFrame: The aggregated cell morphology data.

    Raises:
        EnvironmentError: Raised when GPU is not available on the machine ans use_gpu is True.

    Example:
        ```python
        cell_morphology_ref_df = get_cell_morphology_ref("example_reference", filter)
        aggregated_df = get_cell_morphology_data(cell_morphology_ref_df, aggregation_level='plate')
        display(aggregated_df)
        ```
    """

    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(cell_morphology_ref_df, pd.DataFrame):
        cell_morphology_ref_df = pl.from_pandas(cell_morphology_ref_df)

    if aggregation_method is None:
        aggregation_method = cfg.AGGREGATION_METHOD_DICT

    object_file_names = cfg.OBJECT_FILE_NAMES
    plate_acq_id = cfg.DATABASE_SCHEMA["EXPERIMENT_PLATE_ACQID_COLUMN"]
    plate_acq_name = cfg.DATABASE_SCHEMA["EXPERIMENT_PLATE_AQNAME_COLUMN"]
    experiment_name = (
        cell_morphology_ref_df.select(cfg.DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"])
        .unique()
        .item()
    )

    # Create output directory if it doesn't exist
    saving_dir = Path(path_to_save)
    saving_dir.mkdir(parents=True, exist_ok=True)

    # Set up progress bar for feedback
    total_iterations = cell_morphology_ref_df.height * len(object_file_names)
    progress_bar = tqdm(total=total_iterations, desc="Processing")

    # Check for typpe of aggregation function ans gpu
    if use_gpu and not has_gpu():
        raise EnvironmentError(
            "GPU is not available on this machine."
        )
    aggregation_func = fa.aggregate_data_gpu if use_gpu else fa.aggregate_data_cpu

    per_plate_dataframe_list = []

    # Check if 'all_plates' file exists before entering the loop
    output_filename_all_plates = f"{saving_dir}/{experiment_name}_all_plates.parquet"
    if os.path.exists(output_filename_all_plates):
        log_info(
            f"Combined plates file exists, reading data from: {output_filename_all_plates}"
        )
        return pl.read_parquet(output_filename_all_plates)
    else:
        for index, plate_metadata in enumerate(
            cell_morphology_ref_df.iter_rows(named=True)
        ):
            # Print separator and progress info
            separator = "\n" if index else ""
            log_info(
                (
                    f"{separator}{'_'*50}"
                    f"\nProcessing plate {plate_metadata[plate_acq_name]} ({index + 1} of {cell_morphology_ref_df.height}):"
                )
            )

            # Define and check for existing output files
            output_filename_per_plate = f"{saving_dir}/{plate_metadata[plate_acq_id]}_{plate_metadata[plate_acq_name]}.parquet"
            if os.path.exists(output_filename_per_plate):
                log_info(
                    f"File already exists, reading data from: {output_filename_per_plate}"
                )
                per_plate_dataframe_list.append(
                    pl.read_parquet(output_filename_per_plate)
                )
                progress_bar.update(len(object_file_names))
                continue

            # Load and process feature datasets
            object_feature_dataframes = {}
            unusful_col_pattern = (
                r"^(FileName|PathName|ImageNumber|Number_Object_Number)"
            )
            for object_file_name in object_file_names:
                object_feature_file_path = f"{plate_metadata[cfg.DATABASE_SCHEMA['EXPERIMENT_RESULT_DIRECTORY_COLUMN']]}{object_file_name}.parquet"

                # Read the parquet file and adjust column names
                columns_names = pl.scan_parquet(object_feature_file_path).columns
                object_feature_df = pl.read_parquet(
                    object_feature_file_path,
                    columns=[
                        col
                        for col in columns_names
                        if not re.match(unusful_col_pattern, col)
                    ],
                )

                # Adding object type name to the end of column name
                object_name = object_file_name.split("_")[-1]
                object_feature_df.columns = [
                    f"{col}_{object_name}" for col in object_feature_df.columns
                ]

                object_feature_dataframes[object_name] = object_feature_df
                log_info(
                    f"\tReading features {object_feature_df.shape} - {object_name}: \t{object_feature_file_path}"
                )

                progress_bar.update(1)

            # Join df dictionary (first cell -> nuclei and then -> cytoplasm)
            joined_object_df = _join_object_dataframes(object_feature_dataframes)

            # Remove '_cells' from metadata columns' name for better consistency and clarity
            joined_object_df = _rename_joined_df_columns(joined_object_df)

            # Create unique image_id and cell_id column by concatenating other columns
            joined_object_df = _add_image_cell_id_columns(joined_object_df)

            # Clean df from temporary, unused or unwanted columns
            joined_object_df = _drop_unwanted_columns(joined_object_df)

            # Ensure data type consistency for Metadata columns
            joined_object_df = _cast_metadata_type_columns(joined_object_df)

            # Ordering the columns
            joined_object_df = _reorder_dataframe_columns(joined_object_df)

            # List of morphology columns
            morphology_feature_cols = _get_morphology_feature_cols(joined_object_df)

            # Adding plate layout data to df
            aggregated_data = _merge_with_plate_info(joined_object_df)

            # Mapping of aggregation levels to their grouping columns
            grouping_columns_map = cfg.GROUPING_COLUMN_MAP

            for level in ["cell", "site", "well", "plate"]:
                aggregated_data = aggregation_func(
                    df=aggregated_data,
                    columns_to_aggregate=morphology_feature_cols,
                    groupby_columns=grouping_columns_map[level],
                    aggregation_function=aggregation_method[level],
                )
                if aggregation_level == level:
                    break

            # Write the aggregated data to a parquet file
            if save_plate_separately:
                aggregated_data.write_parquet(output_filename_per_plate)
            per_plate_dataframe_list.append(aggregated_data)

        if not save_plate_separately:
            concatenated_dfs = (
                pl.concat(per_plate_dataframe_list)
                if len(per_plate_dataframe_list) > 1
                else per_plate_dataframe_list[0]
            )
            if aggregation_level == "compound":
                concatenated_dfs = aggregation_func(
                    df=concatenated_dfs,
                    columns_to_aggregate=morphology_feature_cols,
                    groupby_columns=grouping_columns_map[aggregation_level],
                    aggregation_function=aggregation_method[aggregation_level],
                )
            concatenated_dfs.write_parquet(output_filename_all_plates)
            progress_bar.close()
            return concatenated_dfs

    progress_bar.close()

    return (
        pl.concat(per_plate_dataframe_list)
        if len(per_plate_dataframe_list) > 1
        else per_plate_dataframe_list[0]
    )
