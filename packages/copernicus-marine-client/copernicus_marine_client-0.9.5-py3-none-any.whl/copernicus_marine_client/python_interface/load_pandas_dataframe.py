import pathlib
from datetime import datetime
from typing import List, Optional, Union

import pandas

from copernicus_marine_client.catalogue_parser.request_structure import (
    LoadRequest,
)
from copernicus_marine_client.download_functions.download_arco_series import (
    load_pandas_dataframe_from_arco_series,
)
from copernicus_marine_client.download_functions.download_opendap import (
    load_pandas_dataframe_from_opendap,
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
def load_pandas_dataframe(
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
) -> pandas.DataFrame:
    """
    Load a Pandas DataFrame containing Copernicus Marine data from a specified dataset.

    Args:
        dataset_url (str, optional): The URL of the dataset.
        dataset_id (str, optional): The identifier of the dataset.
        username (str, optional): Username for authentication.
        password (str, optional): Password for authentication.
        variables (List[str], optional): List of variable names to load.
        minimal_longitude (float, optional): Minimal longitude for spatial subset.
        maximal_longitude (float, optional): Maximal longitude for spatial subset.
        minimal_latitude (float, optional): Minimal latitude for spatial subset.
        maximal_latitude (float, optional): Maximal latitude for spatial subset.
        minimal_depth (float, optional): Minimal depth for vertical subset.
        maximal_depth (float, optional): Maximal depth for vertical subset.
        vertical_dimension_as_originally_produced (bool, optional): If True, use the vertical dimension as originally produced.
        start_datetime (datetime, optional): Start datetime for temporal subset.
        end_datetime (datetime, optional): End datetime for temporal subset.
        force_service (str, optional): Force a specific service for data download.
        credentials_file (Union[pathlib.Path, str], optional): Path to a credentials file for authentication.
        overwrite_metadata_cache (bool, optional): If True, overwrite the metadata cache.
        no_metadata_cache (bool, optional): If True, do not use metadata caching.

    Returns:
        pandas.DataFrame: A DataFrame containing the loaded Copernicus Marine data.
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
        load_pandas_dataframe_from_arco_series,
        load_pandas_dataframe_from_opendap,
    )
    return dataset
