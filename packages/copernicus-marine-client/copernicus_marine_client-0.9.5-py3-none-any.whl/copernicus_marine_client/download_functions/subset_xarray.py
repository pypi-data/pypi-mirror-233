from datetime import datetime
from decimal import Decimal
from typing import List, Literal, Optional, Union

import numpy as np
import xarray as xr

from copernicus_marine_client.download_functions.subset_parameters import (
    DepthParameters,
    GeographicalParameters,
    LatitudeParameters,
    LongitudeParameters,
    TemporalParameters,
)

COORDINATES_LABEL = {
    "latitude": ["latitude", "nav_lat", "x", "lat"],
    "longitude": ["longitude", "nav_lon", "y", "lon"],
    "time": ["time_counter", "time"],
    "depth": ["depth", "deptht", "elevation"],
}


class MinimalLongitudeGreaterThanMaximalLongitude(Exception):
    pass


def dataset_custom_sel(
    dataset: xr.Dataset,
    coord_type: Literal["latitude", "longitude", "depth", "time"],
    coord_selection: Union[float, slice, datetime, None],
    method: Union[str, None] = None,
) -> xr.Dataset:
    for coord_label in COORDINATES_LABEL[coord_type]:
        if coord_label in dataset.coords:
            dataset = dataset.sel(
                {coord_label: coord_selection}, method=method
            )
    return dataset


def _latitude_subset(
    dataset: xr.Dataset, latitude_parameters: LatitudeParameters
) -> xr.Dataset:
    minimal_latitude = latitude_parameters.minimal_latitude
    maximal_latitude = latitude_parameters.maximal_latitude
    if minimal_latitude is not None or maximal_latitude is not None:
        latitude_selection = (
            minimal_latitude
            if minimal_latitude == maximal_latitude
            else slice(minimal_latitude, maximal_latitude)
        )
        latitude_method = (
            "nearest" if minimal_latitude == maximal_latitude else None
        )
        dataset = dataset_custom_sel(
            dataset, "latitude", latitude_selection, latitude_method
        )
    return dataset


def _longitude_subset(
    dataset: xr.Dataset, longitude_parameters: LongitudeParameters
) -> xr.Dataset:
    def _update_dataset_attributes(dataset: xr.Dataset):
        for coord_label in COORDINATES_LABEL["longitude"]:
            if coord_label in dataset.coords:
                attrs = dataset[coord_label].attrs
                if "valid_min" in attrs:
                    attrs["valid_min"] += 180
                if "valid_max" in attrs:
                    attrs["valid_max"] += 180
                dataset = dataset.assign_coords(
                    {coord_label: dataset[coord_label] % 360}
                ).sortby(coord_label)
                dataset[coord_label].attrs = attrs
        return dataset

    minimal_longitude = longitude_parameters.minimal_longitude
    maximal_longitude = longitude_parameters.maximal_longitude
    if minimal_longitude is not None or maximal_longitude is not None:
        if minimal_longitude is not None and maximal_longitude is not None:
            if minimal_longitude > maximal_longitude:
                raise MinimalLongitudeGreaterThanMaximalLongitude(
                    "--minimal-longitude option must be smaller "
                    "or equal to --maximal-longitude"
                )
            if maximal_longitude - minimal_longitude >= 360:
                longitude_selection: Union[float, slice, None] = None
            elif minimal_longitude == maximal_longitude:
                longitude_selection = longitude_modulus(minimal_longitude)
                longitude_method = "nearest"
            else:
                minimal_longitude_modulus = longitude_modulus(
                    minimal_longitude
                )
                maximal_longitude_modulus = longitude_modulus(
                    maximal_longitude
                )
                if maximal_longitude_modulus < minimal_longitude_modulus:
                    maximal_longitude_modulus += 360
                    dataset = _update_dataset_attributes(dataset)
                longitude_selection = slice(
                    minimal_longitude_modulus,
                    maximal_longitude_modulus,
                )
                longitude_method = None
        else:
            longitude_selection = slice(minimal_longitude, maximal_longitude)
            longitude_method = None

        if longitude_selection is not None:
            dataset = dataset_custom_sel(
                dataset, "longitude", longitude_selection, longitude_method
            )
    return dataset


def _temporal_subset(
    dataset: xr.Dataset, temporal_parameters: TemporalParameters
) -> xr.Dataset:
    start_datetime = temporal_parameters.start_datetime
    end_datetime = temporal_parameters.end_datetime
    if start_datetime is not None or end_datetime is not None:
        temporal_selection = (
            start_datetime
            if start_datetime == end_datetime
            else slice(start_datetime, end_datetime)
        )
        temporal_method = "nearest" if start_datetime == end_datetime else None
        dataset = dataset_custom_sel(
            dataset, "time", temporal_selection, temporal_method
        )
    return dataset


def _depth_subset(
    dataset: xr.Dataset, depth_parameters: DepthParameters
) -> xr.Dataset:
    def convert_elevation_to_depth(dataset: xr.Dataset):
        if "elevation" in dataset.coords:
            attrs = dataset["elevation"].attrs
            dataset = dataset.reindex(elevation=dataset.elevation[::-1])
            dataset["elevation"] = dataset.elevation * (-1)
            dataset = dataset.rename({"elevation": "depth"})
            dataset.depth.attrs = attrs
        return dataset

    if depth_parameters.vertical_dimension_as_originally_produced:
        dataset = convert_elevation_to_depth(dataset)
    minimal_depth = depth_parameters.minimal_depth
    maximal_depth = depth_parameters.maximal_depth
    if minimal_depth is not None or maximal_depth is not None:
        if "elevation" in dataset.coords:
            minimal_depth = (
                minimal_depth * -1.0 if minimal_depth is not None else None
            )
            maximal_depth = (
                maximal_depth * -1.0 if maximal_depth is not None else None
            )
            minimal_depth, maximal_depth = maximal_depth, minimal_depth

        depth_selection = (
            minimal_depth
            if minimal_depth == maximal_depth
            else slice(minimal_depth, maximal_depth)
        )
        depth_method = "nearest" if minimal_depth == maximal_depth else None
        dataset = dataset_custom_sel(
            dataset, "depth", depth_selection, depth_method
        )
    return dataset


def subset(
    dataset: xr.Dataset,
    variables: Optional[List[str]],
    geographical_parameters: GeographicalParameters,
    temporal_parameters: TemporalParameters,
    depth_parameters: DepthParameters,
) -> xr.Dataset:

    if variables:
        dataset = dataset[np.array(variables)]

    dataset = _latitude_subset(
        dataset, geographical_parameters.latitude_parameters
    )
    dataset = _longitude_subset(
        dataset, geographical_parameters.longitude_parameters
    )

    dataset = _temporal_subset(dataset, temporal_parameters)

    dataset = _depth_subset(dataset, depth_parameters)

    return dataset


def longitude_modulus(longitude: float) -> float:
    """
    Returns the equivalent longitude between -180 and 180
    """
    # We are using Decimal to avoid issue with rounding
    modulus = float(Decimal(str(longitude + 180)) % 360)
    # Modulus with python return a negative value if the denominator is negative
    # To counteract that, we add 360 if the result is < 0
    modulus = modulus if modulus >= 0 else modulus + 360
    return modulus - 180
