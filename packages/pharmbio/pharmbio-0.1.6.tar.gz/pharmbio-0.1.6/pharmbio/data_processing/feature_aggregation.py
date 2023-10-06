import polars as pl
import pandas as pd
from typing import Union, List
import importlib
from ..utils import get_gpu_info
from ..logger import (
    log_error,
)


def aggregate_data_cpu(
    df: Union[pl.DataFrame, pd.DataFrame],
    columns_to_aggregate: List[str],
    groupby_columns: List[str],
    aggregation_function: str = "mean",
):
    """
    Aggregates morphology data using the specified columns and aggregation function.

    Args:
        df (Union[pl.DataFrame, pd.DataFrame]): The input DataFrame to be aggregated.
        columns_to_aggregate (List[str]): The list of columns to be aggregated.
        groupby_columns (List[str]): The list of columns to group by.
        aggregation_function (str, optional): The aggregation function to be applied. Defaults to "mean" where
        possible values could set to: "mean", median, "sum", "min", "max".

    Returns:
        pl.DataFrame: The aggregated DataFrame.

    Examples:
        ```python
        df = pd.DataFrame({
            'A': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
            'B': [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2],
            'C': [9, 10, 11, 12, 9, 10, 11, 12, 12, 11, 12],
            'D': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]})

        aggregate_data_cpu(df, columns_to_aggregate=['B', 'C'], groupby_columns=['A'], aggregation_function='mean')
        ```
    """

    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    grouped = df.lazy().groupby(groupby_columns)
    agg_exprs = [
        getattr(pl.col(col), aggregation_function)().alias(col)
        for col in columns_to_aggregate
    ]

    metadata_column = [
        col
        for col in df.columns
        if col not in columns_to_aggregate and col not in groupby_columns
    ]
    metadata_agg_exprs = [pl.col(col).first().alias(col) for col in metadata_column]

    all_agg_exprs = agg_exprs + metadata_agg_exprs

    # Execute the aggregation.
    agg_df = grouped.agg(all_agg_exprs)

    return agg_df.sort(groupby_columns).collect()


def aggregate_data_gpu(
    df: Union[pl.DataFrame, pd.DataFrame],
    columns_to_aggregate: List[str],
    groupby_columns: List[str],
    aggregation_function: str = "mean",
):  # sourcery skip: extract-method
    """
    Aggregates data using the specified columns and aggregation function with GPU acceleration.

    Args:
        df (Union[pl.DataFrame, pd.DataFrame]): The input DataFrame to be aggregated.
        columns_to_aggregate (List[str]): The list of columns to be aggregated.
        groupby_columns (List[str]): The list of columns to group by.
        aggregation_function (str, optional): The aggregation function to be applied. Defaults to "mean" where
        possible values could set to: "mean", median, "sum", "min", "max".

    Returns:
        pl.DataFrame: The aggregated DataFrame.

    Raises:
        ImportError: Raised when Dask-CUDA is not available.
        RuntimeError: Raised when an unexpected error occurs during the aggregation process.

    Example:
        ```python
        df = pd.DataFrame({
            'A': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
            'B': [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2],
            'C': [9, 10, 11, 12, 9, 10, 11, 12, 12, 11, 12],
            'D': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]})

        aggregate_data_gpu(df, columns_to_aggregate=['B', 'C'], groupby_columns=['A'], aggregation_function='mean')
        ```
    """

    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    total_memory, n_gpus = get_gpu_info()

    if total_memory is None and n_gpus is None:
        log_error("Failed to get GPU information.")

    try:
        cp = importlib.import_module("cupy")

        grouped = df.lazy().group_by(groupby_columns)
        agg_exprs = [
                pl.col(col).map_elements(
                lambda x: getattr(cp, aggregation_function)(cp.asarray(x.to_numpy().squeeze()))).alias(col)
        for col in columns_to_aggregate
        ]

        metadata_column = [
            col
            for col in df.columns
            if col not in columns_to_aggregate and col not in groupby_columns
        ]
        metadata_agg_exprs = [pl.col(col).first().alias(col) for col in metadata_column]

        all_agg_exprs = agg_exprs + metadata_agg_exprs

        # Execute the aggregation.
        agg_df = grouped.agg(all_agg_exprs)

        return agg_df.sort(groupby_columns).collect()

    except ImportError as e:
        raise ImportError(
            "cupy package is not available. Please install it with 'pip install cupy' to use GPU acceleration."
        ) from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e
