import logging

import typer

from alvin_cli.config.loader import set_current_config_context
from alvin_cli.config.loader import set_key_value_in_cfg
from alvin_cli.utils.common_arguments import BRIGHT_GREEN_COLOR_TYPER
from alvin_cli.utils.common_arguments import BRIGHT_YELLOW_COLOR_TYPER
from alvin_cli.utils.common_arguments import current_active_profile
from alvin_cli.utils.helper_functions import typer_secho_raise


app = typer.Typer(add_completion=False)

ACTIVE_CONTEXT = current_active_profile


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


@app.command("activate")
def set_current_context(
    section: str = typer.Argument(
        ...,
        help=typer.style("Which config section to use?", fg=BRIGHT_GREEN_COLOR_TYPER),
    )
) -> None:
    """Set current active context in configuration"""
    section = section.upper()
    set_context_exists = set_current_config_context(section)
    if set_context_exists:
        typer_secho_raise(f"Updated current active section to {[section]}", "GREEN")
    else:
        typer_secho_raise(
            f"{[section]} doesnt' exist, create the section first using `alvin config set` command",
            "MAGENTA",
        )


@app.command("set")
def add_and_update_section(
    section: str = typer.Option(
        ACTIVE_CONTEXT,
        help=typer.style(
            "Which section to update? By default current activated section is updated",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    key: str = typer.Argument(
        ..., help=typer.style("Add or update a key", fg=BRIGHT_GREEN_COLOR_TYPER)
    ),
    value: str = typer.Argument(
        ..., help=typer.style("Add or update a value", fg=BRIGHT_GREEN_COLOR_TYPER)
    ),
) -> None:
    """Set keys and values to context in configuration. Also creates inputted section if it doesn't exist"""
    if set_key_value_in_cfg(section, key, value):
        typer_secho_raise(
            f"Updated {section.upper()}/{key} to be {value}", color="GREEN"
        )

    else:
        typer_secho_raise(
            "Something went wrong, run the command with root privileges or check the input format",
            "RED",
        )
