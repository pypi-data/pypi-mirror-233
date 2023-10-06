from sys import displayhook
import polars as pl
import pandas as pd
from collections import defaultdict
from typing import Union, Tuple, Literal, Set, List, Dict
import re
from .utils import normalize_df


DEFAULT_QC_MODULES = {
        "FocusScore",
        "MaxIntensity",
        "MeanIntensity",
        "PowerLogLogSlope",
        "StdIntensity",
    }


def get_qc_module(qc_data: Union[pl.DataFrame, pd.DataFrame]):
    # Collect columns related to image quality
    image_quality_cols = [col for col in qc_data.columns if "ImageQuality_" in col]
    # Remove 'ImageQuality_' prefix from column names
    image_quality_module = [
        col.replace("ImageQuality_", "") for col in image_quality_cols
    ]
    return sorted({re.sub("_.*", "", measure) for measure in image_quality_module})


def get_qc_data_dict(
    qc_data: Union[pl.DataFrame, pd.DataFrame],
    module_to_keep: Set[str] = None,
    module_to_drop: Set[str] = None,
):
    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(qc_data, pd.DataFrame):
        qc_data = pl.from_pandas(qc_data)

    default_module_to_keep = DEFAULT_QC_MODULES

    # If both are None, use default
    if not module_to_keep and not module_to_drop:
        module_to_keep = default_module_to_keep

    # Filter and transform column names
    image_quality_cols = [
        col for col in qc_data.columns if col.startswith("ImageQuality_")
    ]
    image_quality_measures_all = {
        col.replace("ImageQuality_", "").split("_")[0] for col in image_quality_cols
    }

    # Filter out the measures
    image_quality_measures_filtered = {
        measure
        for measure in image_quality_measures_all
        if (not module_to_keep or measure in module_to_keep)
        and (not module_to_drop or measure not in module_to_drop)
    }

    # Create the DataFrame dictionary
    return {
        measure: qc_data.select(
            [col for col in image_quality_cols if f"_{measure}" in col]
        )
        for measure in image_quality_measures_filtered
    }


def get_channels(
    qc_data: Union[pl.DataFrame, pd.DataFrame], qc_module_list: List[str] = None
):
    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(qc_data, pd.DataFrame):
        qc_data = pl.from_pandas(qc_data)

    pattern_digit = re.compile(r"\d+$")
    pattern_digit_letter = re.compile(r"\d+[A-Z]+")
    pattern_sub_channel = re.compile(r"^.*?_.*?_")

    if not qc_module_list:
        qc_module_list = get_qc_module(qc_data)

    result_dict = {}

    for module in qc_module_list:
        channel_list = set()
        sub_channel_list = set()
        data_dict = get_qc_data_dict(qc_data, module_to_keep={module})
        for c in data_dict[module].columns:
            if module in c:
                parts = c.split("_")
                last_part = parts[-1]
                if last_part.isdigit() or pattern_digit_letter.match(last_part):
                    channel = pattern_digit.sub("", parts[-2])
                    sub_channel = pattern_sub_channel.sub("", c)
                    channel_list.add(channel)
                    sub_channel_list.add(sub_channel)
                else:
                    channel_list.add(last_part)

        result_dict[module] = {
            "channels": sorted(channel_list),
            "sub_channels": sorted(sub_channel_list),
        }

    return result_dict


def flag_outlier_images(
    qc_data: Union[pl.DataFrame, pd.DataFrame],
    module_to_keep: Set[str] = None,
    module_to_drop: Set[str] = None,
    method: Literal["SD", "IQR"] = "SD",
    IQR_normalization: bool = True,
    normalization: Literal["zscore", "minmax"] = "zscore",
    sd_step_dict: Dict[str, Tuple[float, float]] = None,
    default_sd_step: Tuple[float, float] = (-4.5, 4.5),
    quantile_limit: float = 0.25,
    multiplier: float = 1.5,
):
    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(qc_data, pd.DataFrame):
        qc_data = pl.from_pandas(qc_data)

    # Create the DataFrame dictionary
    data_frame_dictionary = get_qc_data_dict(qc_data, module_to_keep, module_to_drop)
    module_list = sorted(data_frame_dictionary.keys())

    if not 0 < quantile_limit <= 0.5:
        raise ValueError("quantile_limit must be between 0 and 0.5")

    if multiplier <= 0:
        raise ValueError("multiplier must be a positive value")

    if method == "SD":
        outlier_prefix = "OutlierSD_"
        all_sd_step_dict = defaultdict(lambda: default_sd_step)

        if sd_step_dict:
            for key, value in sd_step_dict.items():
                all_sd_step_dict[key] = value

        for image_quality_name in module_list:
            # Get the current dataframe from the dictionary
            current_dataframe = data_frame_dictionary[image_quality_name]

            # Scale the dataframe values
            current_dataframe_scaled = normalize_df(
                current_dataframe, method=normalization
            )

            # Get the lower and upper treshold for the current image_quality_name
            lower_threshold, upper_threshold = all_sd_step_dict[image_quality_name]

            # Create a new flag
            new_flag_scaled = f"{outlier_prefix}{image_quality_name}_{lower_threshold}_{upper_threshold}"
            outliers = [
                1 if i == True else 0
                for i in current_dataframe_scaled.apply(
                    lambda row: any(
                        (val < lower_threshold) | (val > upper_threshold) for val in row
                    )
                ).to_series()
            ]
            qc_data = qc_data.with_columns(pl.lit(outliers).alias(new_flag_scaled))

        # Identify columns starting with 'OutlierZscore_'
        outlier_flaged_columns = [
            item for item in qc_data.columns if item.startswith(outlier_prefix)
        ]
        flagged_qc_data = qc_data.with_columns(
            pl.max(pl.col(outlier_flaged_columns)).alias("outlier_flag")
        )

    elif method == "IQR":
        outlier_prefix = "OutlierIQR_"

        for image_quality_name in module_list:
            # Get the current dataframe from the dictionary
            current_dataframe = data_frame_dictionary[image_quality_name]

            if IQR_normalization:
                # Scale the dataframe values
                current_dataframe = normalize_df(
                    current_dataframe, method=normalization
                )

            # Calculate the lower and upper quantiles
            lower_quantile = current_dataframe.quantile(quantile_limit)
            upper_quantile = current_dataframe.quantile(1 - quantile_limit)

            # Define the IQR and the bounds for outliers
            IQR = upper_quantile - lower_quantile
            lower_threshold = (lower_quantile - multiplier * IQR).to_numpy().min()
            upper_threshold = (upper_quantile + multiplier * IQR).to_numpy().max()

            # Create a new flag
            new_flag_iqr = f"{outlier_prefix}{image_quality_name}_{round(lower_threshold, 3)}_{round(upper_threshold, 3)}"
            outliers = [
                1 if i == True else 0
                for i in current_dataframe.apply(
                    lambda row: any(
                        (val < lower_threshold) | (val > upper_threshold) for val in row
                    )
                ).to_series()
            ]

            qc_data = qc_data.with_columns(pl.lit(outliers).alias(new_flag_iqr))

        # Identify columns starting with 'OutlierScaled_'
        outlier_flaged_columns = [
            item for item in qc_data.columns if item.startswith(outlier_prefix)
        ]
        flagged_qc_data = qc_data.with_columns(
            pl.max(pl.col(outlier_flaged_columns)).alias("outlier_flag")
        )

    else:
        raise ValueError("Method must be either 'zscore' or 'IQR'")

    # Display the number of flagged image based on each quality module'
    outlier_flaged_columns = [
        col for col in flagged_qc_data.columns if col.startswith(outlier_prefix)
    ]
    displayhook(flagged_qc_data.select(outlier_flaged_columns + ["outlier_flag"]).sum())

    return flagged_qc_data