"""
.
"""

from importlib.metadata import version

__version__ = version("copernicus-marine-client")

from copernicus_marine_client.python_interface.login import login
from copernicus_marine_client.python_interface.describe import describe
from copernicus_marine_client.python_interface.get import get
from copernicus_marine_client.python_interface.subset import subset
from copernicus_marine_client.python_interface.load_xarray_dataset import load_xarray_dataset
from copernicus_marine_client.python_interface.load_pandas_dataframe import load_pandas_dataframe
