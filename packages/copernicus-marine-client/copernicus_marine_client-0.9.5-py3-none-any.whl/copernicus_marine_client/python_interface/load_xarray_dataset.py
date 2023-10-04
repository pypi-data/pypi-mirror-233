import pathlib
from datetime import datetime
from typing import List, Optional, Union

import xarray

from copernicus_marine_client.catalogue_parser.request_structure import (
    LoadRequest,
)
from copernicus_marine_client.download_functions.download_arco_series import (
    load_xarray_dataset_from_arco_series,
)
from copernicus_marine_client.download_functions.download_opendap import (
    load_xarray_dataset_from_opendap,
)
from copernicus_marine_client.download_functions.subset_parameters import (
    DepthParameters,
    GeographicalParameters,
    LatitudeParameters,
    LongitudeParameters,
    TemporalParameters,
)
from copernicus_marine_client.python_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicus_marine_client.python_interface.load_utils import (
    load_data_object_from_load_request,
)


@log_exception_and_exit
def load_xarray_dataset(
    dataset_url: Optional[str] = None,
    dataset_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    variables: Optional[List[str]] = None,
    minimal_longitude: Optional[float] = None,
    maximal_longitude: Optional[float] = None,
    minimal_latitude: Optional[float] = None,
    maximal_latitude: Optional[float] = None,
    minimal_depth: Optional[float] = None,
    maximal_depth: Optional[float] = None,
    vertical_dimension_as_originally_produced: bool = False,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    force_service: Optional[str] = None,
    credentials_file: Optional[Union[pathlib.Path, str]] = None,
    overwrite_metadata_cache: bool = False,
    no_metadata_cache: bool = False,
) -> xarray.Dataset:
    """
    Load an xarray dataset from Copernicus Marine data source.

    This function allows loading an xarray dataset from a Copernicus Marine data source
    using either the ARCO series or OpenDAP protocol. It supports various parameters
    for customization, such as specifying geographical bounds, temporal range,
    depth range, and more.

    Args:
        dataset_url (str, optional): The URL of the dataset. Either `dataset_url` or `dataset_id` should be provided.
        dataset_id (str, optional): The ID of the dataset. Either `dataset_url` or `dataset_id` should be provided.
        username (str, optional): Username for authentication, if required.
        password (str, optional): Password for authentication, if required.
        variables (List[str], optional): List of variable names to be loaded from the dataset.
        minimal_longitude (float, optional): The minimal longitude for subsetting the data.
        maximal_longitude (float, optional): The maximal longitude for subsetting the data.
        minimal_latitude (float, optional): The minimal latitude for subsetting the data.
        maximal_latitude (float, optional): The maximal latitude for subsetting the data.
        minimal_depth (float, optional): The minimal depth for subsetting the data.
        maximal_depth (float, optional): The maximal depth for subsetting the data.
        vertical_dimension_as_originally_produced (bool, optional): If True, use the vertical dimension as originally produced.
        start_datetime (datetime, optional): The start datetime for temporal subsetting.
        end_datetime (datetime, optional): The end datetime for temporal subsetting.
        force_service (str, optional): Force the use of a specific service (ARCO or OpenDAP).
        credentials_file (Union[pathlib.Path, str], optional): Path to a file containing authentication credentials.
        overwrite_metadata_cache (bool, optional): If True, overwrite the metadata cache.
        no_metadata_cache (bool, optional): If True, do not use the metadata cache.

    Returns:
        xarray.Dataset: The loaded xarray dataset.
    """  # noqa
    credentials_file = (
        pathlib.Path(credentials_file) if credentials_file else None
    )
    load_request = LoadRequest(
        dataset_url=dataset_url,
        dataset_id=dataset_id,
        username=username,
        password=password,
        variables=variables,
        geographical_parameters=GeographicalParameters(
            latitude_parameters=LatitudeParameters(
                minimal_latitude=minimal_latitude,
                maximal_latitude=maximal_latitude,
            ),
            longitude_parameters=LongitudeParameters(
                minimal_longitude=minimal_longitude,
                maximal_longitude=maximal_longitude,
            ),
        ),
        temporal_parameters=TemporalParameters(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        ),
        depth_parameters=DepthParameters(
            minimal_depth=minimal_depth,
            maximal_depth=maximal_depth,
            vertical_dimension_as_originally_produced=vertical_dimension_as_originally_produced,  # noqa
        ),
        force_service=force_service,
        credentials_file=credentials_file,
        overwrite_metadata_cache=overwrite_metadata_cache,
        no_metadata_cache=no_metadata_cache,
    )
    dataset = load_data_object_from_load_request(
        load_request,
        load_xarray_dataset_from_arco_series,
        load_xarray_dataset_from_opendap,
    )
    return dataset
