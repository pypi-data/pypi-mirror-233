import logging
import pathlib
from typing import Hashable, Iterable, Optional

import click
import pandas
import xarray
import zarr

from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
)
from copernicus_marine_client.core_functions.utils import (
    FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE,
    construct_query_params_for_marine_data_store_monitoring,
    get_unique_filename,
)
from copernicus_marine_client.download_functions.subset_parameters import (
    DepthParameters,
    GeographicalParameters,
    LatitudeParameters,
    LongitudeParameters,
    TemporalParameters,
)
from copernicus_marine_client.download_functions.subset_xarray import subset


def _rechunk(dataset: xarray.Dataset) -> xarray.Dataset:
    for variable in dataset:
        del dataset[variable].encoding["chunks"]

    vertical_dimension_key = (
        "elevation" if "elevation" in dataset.coords else "depth"
    )
    dataset = dataset.chunk(
        _filter_dimensions(
            _default_rechunks(vertical_dimension_key), dataset.dims.keys()
        )
    )
    return dataset


def _filter_dimensions(
    rechunks: dict[str, int], dimensions: Iterable[Hashable]
) -> dict[str, int]:
    return {k: v for k, v in rechunks.items() if k in dimensions}


def _default_rechunks(vertical_dimension_key: str) -> dict[str, int]:
    return {
        "time": 1,
        vertical_dimension_key: 1,
        "longitude": 500,
        "latitude": 500,
    }


def download_dataset(
    username: str,
    password: str,
    geographical_parameters: GeographicalParameters,
    temporal_parameters: TemporalParameters,
    depth_parameters: DepthParameters,
    dataset_url: str,
    output_directory: pathlib.Path,
    output_filename: pathlib.Path,
    variables: Optional[list[str]],
    force_download: bool = False,
    overwrite_output_data: bool = False,
):
    dataset = _rechunk(
        load_xarray_dataset_from_arco_series(
            username=username,
            password=password,
            dataset_url=dataset_url,
            variables=variables,
            geographical_parameters=geographical_parameters,
            temporal_parameters=temporal_parameters,
            depth_parameters=depth_parameters,
        )
    )

    output_path = pathlib.Path(output_directory, output_filename)

    if not force_download:
        logger = logging.getLogger("blank_logger")
        logger.warn(dataset)
        click.confirm(
            FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE, default=True, abort=True
        )

    output_path = get_unique_filename(
        filepath=output_path, overwrite_option=overwrite_output_data
    )

    write_mode = "w"
    if output_filename.suffix == ".nc":
        if not output_directory.is_dir():
            pathlib.Path.mkdir(output_directory, parents=True)
        dataset.to_netcdf(output_path, mode=write_mode)
    else:
        store = zarr.DirectoryStore(output_path)
        dataset.to_zarr(store=store, mode=write_mode)

    logging.info(f"Successfully downloaded to {output_path}")


def download_zarr(
    username: str,
    password: str,
    subset_request: SubsetRequest,
):
    geographical_parameters = GeographicalParameters(
        latitude_parameters=LatitudeParameters(
            minimal_latitude=subset_request.minimal_latitude,
            maximal_latitude=subset_request.maximal_latitude,
        ),
        longitude_parameters=LongitudeParameters(
            minimal_longitude=subset_request.minimal_longitude,
            maximal_longitude=subset_request.maximal_longitude,
        ),
    )
    temporal_parameters = TemporalParameters(
        start_datetime=subset_request.start_datetime,
        end_datetime=subset_request.end_datetime,
    )
    depth_parameters = DepthParameters(
        minimal_depth=subset_request.minimal_depth,
        maximal_depth=subset_request.maximal_depth,
        vertical_dimension_as_originally_produced=subset_request.vertical_dimension_as_originally_produced,  # noqa
    )
    dataset_url = str(subset_request.dataset_url)
    output_directory = (
        subset_request.output_directory
        if subset_request.output_directory
        else pathlib.Path(".")
    )
    output_filename = (
        subset_request.output_filename
        if subset_request.output_filename
        else pathlib.Path("data.zarr")
    )
    variables = subset_request.variables
    force_download = subset_request.force_download

    download_dataset(
        username=username,
        password=password,
        geographical_parameters=geographical_parameters,
        temporal_parameters=temporal_parameters,
        depth_parameters=depth_parameters,
        dataset_url=dataset_url,
        output_directory=output_directory,
        output_filename=output_filename,
        variables=variables,
        force_download=force_download,
        overwrite_output_data=subset_request.overwrite_output_data,
    )
    return pathlib.Path(output_directory, output_filename)


def load_xarray_dataset_from_arco_series(
    username: str,
    password: str,
    dataset_url: str,
    variables: Optional[list[str]],
    geographical_parameters: GeographicalParameters,
    temporal_parameters: TemporalParameters,
    depth_parameters: DepthParameters,
) -> xarray.Dataset:
    dataset = xarray.open_zarr(
        dataset_url,
        chunks=None,
        # Pass custom query parameters for MDS's Monitoring
        storage_options={
            "params": construct_query_params_for_marine_data_store_monitoring(
                username
            ),
        },
    )
    dataset = subset(
        dataset=dataset,
        variables=variables,
        geographical_parameters=geographical_parameters,
        temporal_parameters=temporal_parameters,
        depth_parameters=depth_parameters,
    )
    return dataset


def load_pandas_dataframe_from_arco_series(
    username: str,
    password: str,
    dataset_url: str,
    variables: Optional[list[str]],
    geographical_parameters: GeographicalParameters,
    temporal_parameters: TemporalParameters,
    depth_parameters: DepthParameters,
) -> pandas.DataFrame:
    dataset = load_xarray_dataset_from_arco_series(
        username=username,
        password=password,
        dataset_url=dataset_url,
        variables=variables,
        geographical_parameters=geographical_parameters,
        temporal_parameters=temporal_parameters,
        depth_parameters=depth_parameters,
    )
    return dataset.to_dataframe()
