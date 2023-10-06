import os
import subprocess
import polars as pl
import pandas as pd
from typing import Union, Literal
from .logger import (
    log_error,
    log_info,
)


def get_file_extension(file_path_name):
    """
    Returns the file extension for the given file path (directory + filename).

    Args:
        file_path_name (str): The path and name of the file without extention.

    Returns:
        Optional[str]: The file extension if the file exists with any of the possible extensions [".parquet", ".csv", ".tsv"], otherwise None.

    Example:
        ```python
        # checking example.csv in data directory
        filename = "data/examlpe"
        extension = get_file_extension(file_path_name)
        print(extension)
        ```
    """
    possible_extensions = [".parquet", ".csv", ".tsv"]
    for ext in possible_extensions:
        full_filename = file_path_name + ext
        if os.path.isfile(full_filename):
            return ext
    return None


def read_file(filename, extension):
    """
    Reads a file with the specified filename and extension and returns a DataFrame.

    Args:
        filename (str): The name of the file to be read.
        extension (str): The extension of the file.

    Returns:
        Union[pl.DataFrame, None]: The DataFrame read from the file, or None if the extension is not supported.

    Example:
        ```python
        filename = "data"
        extension = ".parquet"
        df = read_file(filename, extension)
        print(df)
        ```
    """

    if extension == ".parquet":
        df = pl.read_parquet(filename + extension)
    elif extension in [".csv", ".tsv"]:
        delimiter = "," if extension == ".csv" else "\t"
        df = pl.read_csv(filename + extension, separator=delimiter)
    else:
        return None
    # Change column type to float32 if all values are null (unless in some case it changes to str)
    for name in df.columns:
        if df[name].is_null().sum() == len(df[name]):
            df = df.with_columns(df[name].cast(pl.Float32))
    return df


def normalize_df(
    df: Union[pl.DataFrame, pd.DataFrame],
    method: Literal["zscore", "minmax"] = "zscore",
):
    """
    Normalizes the values in the DataFrame using the specified normalization method.

    Args:
        df (Union[pl.DataFrame, pd.DataFrame]): The input DataFrame to be normalized.
        method (Literal["zscore", "minmax"], optional): The normalization method to be applied. Defaults to "zscore".

    Returns:
        pl.DataFrame: The normalized DataFrame.

    Example:
        ```python
        df = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8],
            'C': [9, 10, 11, 12]
        })
        normalized_df = normalize_df(df, method='minmax')
        print(normalized_df)
        ```
    """

    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    methods = {
        "minmax": lambda x: (x - x.min()) / (x.max() - x.min()),
        "zscore": lambda x: (x - x.mean()) / x.std(ddof=1),
    }

    df = df.select(
        [
            (
                methods[method](df[col])
                if df[col].dtype in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]
                else df[col]
            ).alias(col)
            for col in df.columns
        ]
    )
    return df

def pretty_print_channel_dict(d):
    for module, data in d.items():
        print(module)
        print("  Channels:", data['channels'])
        if data['sub_channels'] != []:
            print("  Sub-channels:", data['sub_channels'])
        print()


def has_gpu():
    """
    Checks if the system has a GPU available using subprocess module and "nvidia-smi".

    Returns:
        bool: True if a GPU is available, False otherwise.
    """
    try:
        subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def get_gpu_info():
    """
    Retrieves GPU information including total memory and GPU count.

    Returns:
        Tuple[Optional[int], Optional[int]]: A tuple containing the total memory in MB and the number of GPUs.

    Example:
        ```python
        total_memory, gpu_count = get_gpu_info()
        print(f"Total Memory: {total_memory} MB")
        print(f"Number of GPUs: {gpu_count}")
        ```
    """

    try:
        nvidia_smi_output = subprocess.check_output("nvidia-smi -q", shell=True).decode(
            "utf-8"
        )

        # Split the output into lines
        lines = nvidia_smi_output.splitlines()

        # Find the line that contains total memory information
        for i, line in enumerate(lines):
            if "FB Memory Usage" in line:
                total_memory_line = lines[i + 1]
                break

        # Extract total memory value
        total_memory = int(total_memory_line.split(":")[1].split()[0])

        # Count GPUs
        gpu_count = nvidia_smi_output.count("Product Name")
        
        log_info(f"Found {gpu_count} gpu/s with total memory of {total_memory} MB!")

        return total_memory, gpu_count
    except Exception as e:
        log_error(f"Failed to execute or parse nvidia-smi command. Error: {e}")
        return None, None
