import logging
import logging.config
import pathlib
import sys
from datetime import datetime
from typing import List, Optional

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineDatasetServiceType,
    get_dataset_and_suffix_path_from_url,
    parse_catalogue,
)
from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
    convert_motu_api_request_to_structure,
    subset_request_from_file,
)
from copernicus_marine_client.core_functions.credentials_utils import (
    get_and_check_username_password,
)
from copernicus_marine_client.core_functions.services_utils import (
    CommandType,
    get_dataset_service_and_suffix_path,
)
from copernicus_marine_client.download_functions.download_arco_series import (
    download_zarr,
)
from copernicus_marine_client.download_functions.download_motu import (
    download_motu,
)
from copernicus_marine_client.download_functions.download_opendap import (
    download_opendap,
)


def subset_function(
    dataset_url: Optional[str],
    dataset_id: Optional[str],
    username: Optional[str],
    password: Optional[str],
    variables: Optional[List[str]],
    minimal_longitude: Optional[float],
    maximal_longitude: Optional[float],
    minimal_latitude: Optional[float],
    maximal_latitude: Optional[float],
    minimal_depth: Optional[float],
    maximal_depth: Optional[float],
    vertical_dimension_as_originally_produced: bool,
    start_datetime: Optional[datetime],
    end_datetime: Optional[datetime],
    output_filename: Optional[pathlib.Path],
    force_service: Optional[str],
    request_file: Optional[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    credentials_file: Optional[pathlib.Path],
    motu_api_request: Optional[str],
    force_download: bool,
    overwrite_output_data: bool,
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
) -> pathlib.Path:
    subset_request = SubsetRequest()
    if request_file:
        subset_request = subset_request_from_file(request_file)
    if motu_api_request:
        motu_api_subset_request = convert_motu_api_request_to_structure(
            motu_api_request
        )
        subset_request.update(motu_api_subset_request.__dict__)
    request_update_dict = {
        "dataset_url": dataset_url,
        "dataset_id": dataset_id,
        "variables": variables,
        "minimal_longitude": minimal_longitude,
        "maximal_longitude": maximal_longitude,
        "minimal_latitude": minimal_latitude,
        "maximal_latitude": maximal_latitude,
        "minimal_depth": minimal_depth,
        "maximal_depth": maximal_depth,
        "vertical_dimension_as_originally_produced": vertical_dimension_as_originally_produced,  # noqa
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "output_filename": output_filename,
        "force_service": force_service,
        "output_directory": output_directory,
    }
    subset_request.update(request_update_dict)
    username, password = get_and_check_username_password(
        username,
        password,
        credentials_file,
    )
    if all(
        e is None
        for e in [
            subset_request.variables,
            subset_request.minimal_longitude,
            subset_request.maximal_longitude,
            subset_request.minimal_latitude,
            subset_request.maximal_latitude,
            subset_request.minimal_depth,
            subset_request.maximal_depth,
            subset_request.start_datetime,
            subset_request.end_datetime,
        ]
    ):
        if not subset_request.dataset_id:
            if subset_request.dataset_url:
                catalogue = parse_catalogue(
                    overwrite_metadata_cache, no_metadata_cache
                )
                (dataset, _,) = get_dataset_and_suffix_path_from_url(
                    catalogue, subset_request.dataset_url
                )
                dataset_id = dataset.dataset_id
            else:
                syntax_error = SyntaxError(
                    "Must specify at least one of "
                    "'dataset_url' or 'dataset_id' options"
                )
                raise syntax_error
        logging.error(
            "Missing subset option. Try 'copernicus-marine subset --help'."
        )
        logging.info(
            "To retrieve a complete dataset, please use instead: "
            f"copernicus-marine get --dataset-id {subset_request.dataset_id}"
        )
        sys.exit(1)
    # Specific treatment for default values:
    # In order to not overload arguments with default values
    if force_download:
        subset_request.force_download = force_download
    if overwrite_output_data:
        subset_request.overwrite_output_data = overwrite_output_data

    catalogue = parse_catalogue(overwrite_metadata_cache, no_metadata_cache)
    dataset_service, _ = get_dataset_service_and_suffix_path(
        catalogue,
        subset_request.dataset_id,
        subset_request.dataset_url,
        subset_request.force_service,
        CommandType.SUBSET,
        subset_request.get_time_and_geographical_subset(),
    )
    subset_request.dataset_url = dataset_service.uri
    logging.info(
        "Downloading using service "
        f"{dataset_service.service_type.service_name.value}..."
    )
    if dataset_service.service_type in [
        CopernicusMarineDatasetServiceType.GEOSERIES,
        CopernicusMarineDatasetServiceType.TIMESERIES,
    ]:
        output_path = download_zarr(
            username,
            password,
            subset_request,
        )
    elif (
        dataset_service.service_type
        == CopernicusMarineDatasetServiceType.OPENDAP
    ):
        output_path = download_opendap(
            username,
            password,
            subset_request,
        )
    elif (
        dataset_service.service_type == CopernicusMarineDatasetServiceType.MOTU
    ):
        output_path = download_motu(
            username,
            password,
            subset_request,
            catalogue=catalogue,
        )
    return output_path
