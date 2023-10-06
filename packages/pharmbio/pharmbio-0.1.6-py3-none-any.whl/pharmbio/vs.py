import polars as pl
import pandas as pd
import plotly.figure_factory as ff
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from collections import defaultdict
from typing import Union, Literal, Tuple, Set, List, Dict
from .qc import get_channels, get_qc_data_dict, DEFAULT_QC_MODULES
from .utils import normalize_df

COLORS = px.colors.qualitative.Set1


def plate_heatmap(
    df: Union[pl.DataFrame, pd.DataFrame],
    plate_names: List[str] = None,
    subplot_num_columns: int = 2,
    plot_size: int = 400,
    measurement: str = "Count_nuclei",
    plate_well_columns: Dict[str, str] = None,
):
    if plate_well_columns is None:
        plate_well_columns = {
            "plates": "Metadata_Barcode",
            "wells": "Metadata_Well",
        }
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    wells = (
        df.select("Metadata_Well")
        .unique()
        .sort(by="Metadata_Well")
        .to_series()
        .to_list()
    )
    rows = sorted(list({w[0] for w in wells}))
    columns = sorted(list({w[1:] for w in wells}))

    if plate_names is None:
        try:
            plate_names = (
                df.select(plate_well_columns["plates"])
                .unique()
                .sort(by=plate_well_columns["plates"])
                .to_series()
                .to_list()
            )
            print(plate_names)
        except Exception:
            print("Plate names is not specified")
            plate_names = []

    # Define the font ratio and number of rows for the grid
    font_ratio = plot_size / 400
    subplot_num_rows = -(
        -len(plate_names) // subplot_num_columns
    )  # Ceiling division to get number of rows needed

    titles = [f"{measurement} for {name} " for name in plate_names]

    # Create a subplot with subplot_num_rows rows and subplot_num_columns columns
    fig = sp.make_subplots(
        rows=subplot_num_rows,
        cols=subplot_num_columns,
        subplot_titles=titles,
    )

    for index, plate in enumerate(plate_names):
        plate_data = df.filter(pl.col(plate_well_columns["plates"]) == plate)
        heatmap_data = []
        heatmap_data_annot = []
        for row in rows:
            heatmap_row = []
            heatmap_row_annot = []
            for column in columns:
                well = row + column
                count_nuclei = plate_data.filter(
                    pl.col(plate_well_columns["wells"]) == well
                )[measurement].to_numpy()

                if count_nuclei.size == 0:
                    well_nuclei_count = 0
                else:
                    well_nuclei_count = (
                        np.mean(count_nuclei).round(decimals=0).astype(int)
                    )

                heatmap_row.append(well_nuclei_count)
                heatmap_row_annot.append(f"{well}: {well_nuclei_count}")
            heatmap_data.append(heatmap_row)
            heatmap_data_annot.append(heatmap_row_annot)

        # Calculate the subplot row and column indices
        subplot_row = index // subplot_num_columns + 1
        subplot_col = index % subplot_num_columns + 1

        heatmap = ff.create_annotated_heatmap(
            heatmap_data,
            x=[str(i + 1) for i in range(24)],
            y=rows,
            annotation_text=heatmap_data,
            colorscale="OrRd",
            hovertext=heatmap_data_annot,
            hoverinfo="text",
        )

        # Add the heatmap to the subplot
        fig.add_trace(heatmap.data[0], row=subplot_row, col=subplot_col)

    # Update x and y axes properties
    for i in fig["layout"]["annotations"]:
        i["font"] = dict(size=12 * font_ratio)
    fig.update_xaxes(tickfont=dict(size=10 * font_ratio), nticks=48, side="bottom")
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
    # fig.update_yaxes(tickfont=dict(size=10*font_ratio))

    # Add the new lines here to adjust annotation positions
    for ann in fig.layout.annotations:
        ann.update(y=ann.y + 0.02)

    fig.update_layout(
        height=plot_size * subplot_num_rows,
        width=plot_size * 1.425 * subplot_num_columns,
    )
    fig.show()


def _lineplot(
    data_frames: pl.DataFrame,
    colors: List[str],
    title: str,
    plot_size: int = 1400,
    normalization: bool = True,
    normalization_method: Literal["zscore", "minmax"] = "zscore",
    y_axis_range: Tuple = (-5, 5),
):
    fig = sp.make_subplots(
        rows=len(data_frames),
        cols=1,
        subplot_titles=[df[0] for df in data_frames],
        x_title="Plates",
    )

    for x in range(len(data_frames)):
        _, channel_names, raw_data = data_frames[x]
        CurrentDataFrame = (
            normalize_df(raw_data, method=normalization_method)
            if normalization
            else raw_data
        )

        min_val = CurrentDataFrame.min().to_numpy().min()  # minimum of all columns
        max_val = CurrentDataFrame.max().to_numpy().max()  # maximum of all columns
        y_axis_range = y_axis_range if normalization else (min_val, max_val)

        for i, column in enumerate(CurrentDataFrame.columns):
            channel_name = channel_names[i]
            show_in_legend = x == 0

            fig.add_trace(
                go.Scatter(
                    x=[str(j) for j in range(CurrentDataFrame.height)],
                    y=CurrentDataFrame[column],
                    mode="lines",
                    line=dict(width=0.5, color=colors[i % len(colors)]),
                    showlegend=False,
                    name=""
                    if show_in_legend
                    else channel_name,  # get the legend just for the first row
                    legendgroup=channel_name,
                ),
                row=x + 1,
                col=1,
            )

        fig.update_xaxes(
            range=[0, CurrentDataFrame.height], showticklabels=False, row=x + 1, col=1
        )
        fig.update_yaxes(range=y_axis_range, row=x + 1, col=1)

        fig.add_shape(
            type="line",
            xref="x",
            yref="paper",
            x0=CurrentDataFrame.height / 2,
            y0=y_axis_range[0],
            x1=CurrentDataFrame.height / 2,
            y1=y_axis_range[1],
            line=dict(
                color="Black",
                width=1,
                dash="dashdot",
            ),
            row=x + 1,
            col=1,
        )

    # Dummy traces for the legend
    for i, channel_name in enumerate(channel_names):
        fig.add_trace(
            go.Scatter(
                x=[None],  # these traces won't appear
                y=[None],
                mode="lines",
                line=dict(
                    width=3, color=colors[i % len(colors)]
                ),  # this will be the width in the legend
                legendgroup=channel_name,
                name=channel_name,  # this will be the name in the legend
            ),
        )

    # Add main title
    fig.update_layout(
        height=1.8 * (len(data_frames) + 1) * 100,
        title_text=title,
        title_x=0.1,
        width=plot_size,
    )

    fig.show()


def quality_module_lineplot(
    df: Union[pl.DataFrame, pd.DataFrame],
    qc_module_to_plot: Set[str] = None,
    title: str = "Unnamed",
    plot_size: int = 1400,
    normalization: bool = True,
    normalization_method: Literal["zscore", "minmax"] = "zscore",
    y_axis_range: Tuple = (-5, 5),
    colors: List[str] = COLORS,
):
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    if not qc_module_to_plot:
        qc_module_to_plot = DEFAULT_QC_MODULES

    title = f"{title} scaled" if normalization else f"{title} raw data"
    image_quality_measures = sorted(list(qc_module_to_plot))
    data_frame_dictionary = get_qc_data_dict(df, module_to_keep=qc_module_to_plot)
    channel_dict = get_channels(df, qc_module_list=image_quality_measures)

    channel_data_frames = defaultdict(list)
    subchannel_data_frames = defaultdict(list)

    for i in image_quality_measures:
        if channel_dict[i]["sub_channels"] != []:
            channel_names = tuple(sorted(channel_dict[i]["sub_channels"]))
            subchannel_data_frames[channel_names].append(
                (i, channel_dict[i]["sub_channels"], data_frame_dictionary.get(i))
            )
        else:
            channel_names = tuple(sorted(channel_dict[i]["channels"]))
            channel_data_frames[channel_names].append(
                (i, channel_dict[i]["channels"], data_frame_dictionary.get(i))
            )

    # Then, create figures for each group of data frames
    for data_frames in channel_data_frames.values():
        _lineplot(
            data_frames,
            colors=colors,
            title=title,
            plot_size=plot_size,
            normalization=normalization,
            normalization_method=normalization_method,
            y_axis_range=y_axis_range,
        )

    for data_frames in subchannel_data_frames.values():
        _lineplot(
            data_frames,
            colors=colors,
            title=title,
            plot_size=plot_size,
            normalization=normalization,
            normalization_method=normalization_method,
            y_axis_range=y_axis_range,
        )