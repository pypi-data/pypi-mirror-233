from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class LatitudeParameters:
    minimal_latitude: Optional[float] = None
    maximal_latitude: Optional[float] = None


@dataclass
class LongitudeParameters:
    minimal_longitude: Optional[float] = None
    maximal_longitude: Optional[float] = None


@dataclass
class GeographicalParameters:
    latitude_parameters: LatitudeParameters = field(
        default_factory=LatitudeParameters
    )
    longitude_parameters: LongitudeParameters = field(
        default_factory=LongitudeParameters
    )


@dataclass
class TemporalParameters:
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None


@dataclass
class DepthParameters:
    minimal_depth: Optional[float] = None
    maximal_depth: Optional[float] = None
    vertical_dimension_as_originally_produced: bool = True
