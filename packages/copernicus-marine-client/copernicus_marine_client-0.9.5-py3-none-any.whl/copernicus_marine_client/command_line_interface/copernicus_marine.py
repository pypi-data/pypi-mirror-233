import json
import logging
import logging.config
import pathlib

import click

from copernicus_marine_client.command_line_interface.group_describe import (
    cli_group_describe,
)
from copernicus_marine_client.command_line_interface.group_get import (
    cli_group_get,
)
from copernicus_marine_client.command_line_interface.group_login import (
    cli_group_login,
)
from copernicus_marine_client.command_line_interface.group_subset import (
    cli_group_subset,
)

log_configuration_dict = json.load(
    open(
        pathlib.Path(pathlib.Path(__file__).parent, "..", "logging_conf.json")
    )
)
logging.config.dictConfig(log_configuration_dict)


@click.command(
    cls=click.CommandCollection,
    sources=[
        cli_group_describe,
        cli_group_login,
        cli_group_subset,
        cli_group_get,
    ],
)
@click.version_option(
    None, "-V", "--version", package_name="copernicus-marine-client"
)
def base_command_line_interface():
    pass


def command_line_interface():
    base_command_line_interface(windows_expand_args=False)


if __name__ == "__main__":
    command_line_interface()
