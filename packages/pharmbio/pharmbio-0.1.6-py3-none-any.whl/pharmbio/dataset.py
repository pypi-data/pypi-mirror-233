import os
import re
import polars as pl
from tqdm.notebook import tqdm
from typing import Union, Tuple, Literal, Set, List, Dict
from .qc import flag_outlier_images, get_qc_module, get_qc_data_dict, get_channels
from .vs import quality_module_lineplot, plate_heatmap, COLORS
from pharmbio import config


def get_projects_list(lookup: str = None):
    query = """
        SELECT project
        FROM image_analyses_per_plate
        GROUP BY project
        ORDER BY project 
        """
    project_list = pl.read_database(query, config.DB_URI).to_dict(as_series=False)["project"]
    project_list = list(filter(None, project_list))
    if lookup is not None:
        lookup = lookup.lower()
        project_list = [s for s in project_list if lookup in s.lower()]
    return project_list


def get_image_quality_info(
    name: str,
    drop_replication: Union[str, List[int]] = "Auto",
    keep_replication: Union[str, List[int]] = "None",
    filter: dict = None,
):  # sourcery skip: low-code-quality
    # Query database and store result in Polars dataframe
    query = f"""
            SELECT *
            FROM image_analyses_per_plate
            WHERE project ILIKE '%%{name}%%'
            AND meta->>'type' = 'cp-qc'
            AND analysis_date IS NOT NULL
            ORDER BY plate_barcode 
            """
    image_quality_info_df = pl.read_database(query, DB_URI)
    data_dict = (
        image_quality_info_df.select(["project", "plate_barcode"])
        .groupby("project")
        .agg(pl.col("plate_barcode"))
        .to_dicts()
    )
    unique_project_count = image_quality_info_df.unique("project").height
    if unique_project_count == 0:
        message = f"Quering the db for {name} returned nothing."
    elif unique_project_count > 1:
        message = f"Quering the db for {name} found {unique_project_count} studies: {image_quality_info_df.unique('project')['project'].to_list()}"
    else:
        message = f"Quering the db for {name} found {unique_project_count} study: {image_quality_info_df.unique('project')['project'].to_list()}"
    print(f"{message}\n{'_'*50}")
    if unique_project_count != 0:
        for i, study in enumerate(data_dict, start=1):
            print(i)
            for value in study.values():
                print("\t" + str(value))
    print("_" * 50)
    grouped_replicates = image_quality_info_df.groupby("plate_barcode")
    for plate_name, group in grouped_replicates:
        if len(group) > 1:
            print(
                f"Analysis for the plate with barcode {plate_name} is replicated {len(group)} times with analysis_id of {sorted(group['analysis_id'].to_list())}"
            )
    if image_quality_info_df.filter(pl.col("plate_barcode").is_duplicated()).is_empty():
        print("No replicated analysis has been found!")
    if drop_replication == "Auto" and keep_replication == "None":
        # keeping the highest analysis_id value of replicated rows
        image_quality_info_df = (
            image_quality_info_df.sort("analysis_id", descending=True)
            .unique("plate_barcode", keep="first")
            .sort("analysis_id")
        )
    elif isinstance(drop_replication, list):
        # drop rows by analysis_id
        image_quality_info_df = image_quality_info_df.filter(~pl.col("analysis_id").is_in(drop_replication))
    elif isinstance(keep_replication, list):
        # drop rows by analysis_id
        image_quality_info_df = image_quality_info_df.filter(pl.col("analysis_id").is_in(keep_replication))

    if filter is None:
        return image_quality_info_df
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
    return image_quality_info_df.filter(final_condition)


def _get_file_extension(filename):
    """Helper function to get file extension"""
    possible_extensions = [".parquet", ".csv", ".tsv"]
    for ext in possible_extensions:
        full_filename = filename + ext
        if os.path.isfile(full_filename):
            return ext
    print(
        f"Warning: No file with extensions {possible_extensions} was not found for {filename}."
    )
    return None


def _read_file(filename, extension):
    """Helper function to read file based on its extension"""
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


def get_image_quality_data(
    filtered_image_quality_info: pl.DataFrame, force_merging_columns: Union[bool, str] = False
):
    # Add qc_file column based on 'results' and 'plate_barcode' columns
    filtered_image_quality_info = filtered_image_quality_info.with_columns(
        (pl.col("results") + "qcRAW_images_" + pl.col("plate_barcode")).alias("qc_file")
    )
    print("\n")
    # Read and process all the files in a list, skipping files not found
    dfs = []
    for row in filtered_image_quality_info.iter_rows(named=True):
        ext = _get_file_extension(row["qc_file"])
        if ext is not None:
            df = _read_file(row["qc_file"], ext)
            df = df.with_columns(
                pl.lit(row["plate_acq_id"]).alias("Metadata_AcqID"),
                pl.lit(row["plate_barcode"]).alias("Metadata_Barcode"),
            )
            # Cast all numerical f64 columns to f32
            for name, dtype in zip(df.columns, df.dtypes):
                if dtype == pl.Float64:
                    df = df.with_columns(pl.col(name).cast(pl.Float32))
                elif dtype == pl.Int64:
                    df = df.with_columns(pl.col(name).cast(pl.Int32))
            dfs.append(df)
            print(f"Successfully imported {df.shape}: {row['qc_file']}{ext}")

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
            print("\nDataframes have different shapes and cannot be stacked together!")
            return None
        concat_method = "vertical"  # standard vertical concatenation

    print(f"\n{'_'*50}\nQuality control data of {len(dfs)} plates imported!\n")
    # Concatenate all the dataframes at once and return it
    return (
        pl.concat(dfs, how=concat_method)
        .with_columns(
            (
                pl.col("Metadata_AcqID").cast(pl.Utf8)
                + "_"
                + pl.col("Metadata_Well")
                + "_"
                + pl.col("Metadata_Site").cast(pl.Utf8)
            ).alias("ImageID")
        )
        .sort(["Metadata_Barcode", "Metadata_Well", "Metadata_Site", "ImageID"])
        if dfs
        else None
    )


class QC:
    def __init__(
        self,
        name: str,
        drop_replication: Union[str, List[int]] = "Auto",
        keep_replication: Union[str, List[int]] = "None",
        force_merging_columns: Union[bool, str] = False,
        filter: dict = None,
    ) -> None:
        self.image_quality_info = get_image_quality_info(name, drop_replication, keep_replication, filter)
        self.image_quality_data = get_image_quality_data(self.image_quality_info, force_merging_columns=force_merging_columns)
        self.project = sorted(self.image_quality_info["project"].unique().to_list())
        self.project_name = self.project[0] if len(self.project) == 1 else None
        self.pipeline_name = sorted(self.image_quality_info["pipeline_name"].unique().to_list())
        self.analysis_date = sorted(self.image_quality_info["analysis_date"].unique().to_list())
        self.plate_barcode = sorted(self.image_quality_info["plate_barcode"].unique().to_list())
        self.plate_acq_name = sorted(self.image_quality_info["plate_acq_name"].unique().to_list())
        self.plate_acq_id = sorted(self.image_quality_info["plate_acq_id"].unique().to_list())
        self.analysis_id = sorted(self.image_quality_info["analysis_id"].unique().to_list())
        if self.image_quality_data is not None:
            self.plate_wells = (
                self.image_quality_data.select("Metadata_Well")
                .unique()
                .sort(by="Metadata_Well")
                .to_series()
                .to_list()
            )
            self.plate_rows = sorted(list({w[0] for w in self.plate_wells}))
            self.plate_columns = sorted(list({w[1:] for w in self.plate_wells}))
            self.image_quality_module = get_qc_module(self.image_quality_data)

    def flag_outlier_images(
        self,
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
        return flag_outlier_images(
            self.image_quality_data,
            module_to_keep,
            module_to_drop,
            method,
            IQR_normalization,
            normalization,
            sd_step_dict,
            default_sd_step,
            quantile_limit,
            multiplier,
        )

    def image_quality_module_data_dict(
        self,
        module_to_keep: Set[str] = None,
        module_to_drop: Set[str] = None,
    ):
        return get_qc_data_dict(
            self.image_quality_data,
            module_to_keep,
            module_to_drop,
        )

    def channels(
        self,
        qc_module_list: List[str] = None,
    ):
        d = get_channels(self.image_quality_data, qc_module_list)
        for module, data in d.items():
            print(module)
            print("  Channels:", data["channels"])
            if data["sub_channels"] != []:
                print("  Sub-channels:", data["sub_channels"])
            print()
        return d

    def plate_heatmap(
        self,
        plate_names: List[str] = None,
        subplot_num_columns: int = 2,
        plot_size: int = 400,
        measurement: str = "Count_nuclei",
    ):
        if not plate_names:
            plate_names = self.plate_barcode
        return plate_heatmap(
            self.image_quality_data,
            plate_names,
            subplot_num_columns,
            plot_size,
            measurement,
        )

    def quality_module_lineplot(
        self,
        qc_module_to_plot: Set[str] = None,
        title: str = None,
        plot_size: int = 1400,
        normalization: bool = True,
        normalization_method: Literal["zscore", "minmax"] = "zscore",
        y_axis_range: Tuple = (-5, 5),
        colors: List[str] = COLORS,
    ):
        if not title:
            title = self.project_name
        return quality_module_lineplot(
            self.image_quality_data,
            qc_module_to_plot,
            title,
            plot_size,
            normalization,
            normalization_method,
            y_axis_range,
            colors,
        )


def get_morphology_info(
    name: str,
    filter: dict = None,
):
    query = f"""
            SELECT *
            FROM image_analyses_per_plate
            WHERE project ILIKE '%%{name}%%'
            AND meta->>'type' = 'cp-features'
            AND analysis_date IS NOT NULL
            ORDER BY plate_acq_id, analysis_id
            """
    df = pl.read_database(query, DB_URI)

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


def get_morphology_data(
    saving_dir: str,
    cp_info_df: pl.DataFrame,
    object_names: List[str] = None,
    aggregation_method: str = "mean",
) -> pl.DataFrame:
    
    # Create output directory if it doesn't exist
    if not os.path.exists(saving_dir):
        os.makedirs(saving_dir)

    if object_names is None:
        object_names = ["featICF_nuclei", "featICF_cells", "featICF_cytoplasm"]
        
    # Dynamically change the plate_name_prefix based on the aggregation method
    if aggregation_method == "mean":
        plate_name_prefix = 'Image_Mean'
    elif aggregation_method == "median":
        plate_name_prefix = 'Image_Median'
    else:
        raise ValueError(f"Unsupported aggregation method: {aggregation_method}")

    # Set up progress bar for feedback
    total_iterations = cp_info_df.height * len(object_names)
    progress_bar = tqdm(total=total_iterations, desc="Processing")
    
    all_dataframes = []

    for index, plate_metadata in enumerate(cp_info_df.iter_rows(named=True)):
        separator = "\n" if index else ""
        print(f"{separator}{'_'*50}", flush=True)
        print(f'Processing plate {plate_metadata["plate_acq_name"]} ({index + 1} of {cp_info_df.height}):', flush=True)
        
        output_filename = f'{saving_dir}/{plate_name_prefix}_{plate_metadata["plate_acq_name"]}.parquet'
        if os.path.exists(output_filename):
            print(f'File already exists, reading data from: {output_filename}', flush=True)
            existing_df = pl.read_parquet(output_filename)
            all_dataframes.append(existing_df)
            progress_bar.update(len(object_names))
            continue

        feature_dataframes = {}
        for feature in object_names:
            feature_file_path = f"{plate_metadata['results']}{feature}.parquet"
            df_feature = pl.read_parquet(feature_file_path)
            cleaned_feature_name = re.sub('_.*', '', re.sub('featICF_', '', feature))
            df_feature.columns = [f"{col}_{cleaned_feature_name}" for col in df_feature.columns]
            
            feature_dataframes[feature] = df_feature
            print(f'\tReading features {df_feature.shape} - {feature[8:]}: \t{feature_file_path}', flush=True)
            
            progress_bar.update(1)
        
        print('Merging the data', flush=True)    
        # Join nuclei and cell data on specified columns
        df_combined = feature_dataframes['featICF_nuclei'].join(
            feature_dataframes['featICF_cells'],
            left_on=['Metadata_Barcode_nuclei', 'Metadata_Site_nuclei', 'Metadata_Well_nuclei', 'Parent_cells_nuclei'],
            right_on=['Metadata_Barcode_cells', 'Metadata_Site_cells', 'Metadata_Well_cells', 'ObjectNumber_cells'],
            how='left', suffix='_cells'
        )

        # Further join with cytoplasm data on specified columns
        df_combined = df_combined.join(
            feature_dataframes['featICF_cytoplasm'],
            left_on=['Metadata_Barcode_nuclei', 'Metadata_Site_nuclei', 'Metadata_Well_nuclei', 'Parent_cells_nuclei'],
            right_on=['Metadata_Barcode_cytoplasm', 'Metadata_Site_cytoplasm', 'Metadata_Well_cytoplasm', 'ObjectNumber_cytoplasm'],
            how='left', suffix='_cytoplasm'
        )

        # Add plate and barcode information to the dataframe
        metadata_cols = [
            pl.lit(plate_metadata['plate_acq_id']).alias("Metadata_AcqID_nuclei"),
            pl.lit(plate_metadata['plate_barcode']).alias("Metadata_Barcode_nuclei")
        ]
        df_combined = df_combined.with_columns(metadata_cols)

        # Renaming columns for better consistency
        rename_map = {
            'Metadata_Barcode_nuclei': 'Metadata_Barcode',
            'Metadata_Well_nuclei': 'Metadata_Well',
            'Metadata_Site_nuclei': 'Metadata_Site',
            'Metadata_AcqID_nuclei': 'Metadata_AcqID'
        }
        df_combined = df_combined.rename(rename_map)

        # Create ImageID column by concatenating other columns
        image_id = (df_combined['Metadata_AcqID'] + '_' + 
                    df_combined['Metadata_Barcode'] + '_' + 
                    df_combined['Metadata_Well'] + '_' + 
                    df_combined['Metadata_Site']).alias("ImageID")
        df_combined = df_combined.with_columns([image_id])

        # Ensure data type consistency for certain columns
        cast_cols = [
            pl.col('Metadata_AcqID').cast(pl.Utf8),
            pl.col('Metadata_Site').cast(pl.Utf8),
        ]
        df_combined = df_combined.with_columns(cast_cols)

        # Group by image-related columns and aggregate the numeric columns
        numeric_columns = [name for name in df_combined.columns if df_combined[name].is_numeric()]
        grouping_cols = ['ImageID', 'Metadata_Barcode', 'Metadata_Well', 'Metadata_Site', 'Metadata_AcqID']

        if aggregation_method == 'mean':
            aggregations = [pl.col(column).mean().alias(column) for column in numeric_columns]
        elif aggregation_method == 'median':
            aggregations = [pl.col(column).median().alias(column) for column in numeric_columns]

        grouped_data = df_combined.groupby(grouping_cols).agg(*aggregations).sort('ImageID')

        grouped_data.write_parquet(output_filename)
        all_dataframes.append(grouped_data)

    progress_bar.close()

    if len(all_dataframes) > 1:
        return pl.concat(all_dataframes)
    else:
        return all_dataframes[0]
    
class CP:
    def __init__(
        self,
        name: str,
        saving_dir: str = "data",
        filter: dict = None,
        feature_names: List[str] = None,
    ) -> None:
        
        if feature_names is None:
            feature_names = ["featICF_nuclei", "featICF_cells", "featICF_cytoplasm"]
