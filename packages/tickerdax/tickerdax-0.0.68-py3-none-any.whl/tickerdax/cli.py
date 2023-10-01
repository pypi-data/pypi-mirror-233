import os
import typer
import tickerdax
import tomlkit
import art
import json
import yaml
import importlib.metadata
from pathlib import Path
from rich import print
from rich.text import Text
from typing import Optional, List
from tickerdax import formatting
from tickerdax.constants import Envs, Default, ConfigFormats, EXAMPLE_CONFIG_DATA
from tickerdax.client import TickerDax
from tickerdax.streamer import Streamer
from tickerdax.downloader import Downloader
from typer import rich_utils
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing_extensions import Annotated

# load in the env file if there is one
load_dotenv('.env')

# monkey patch this function, so we can add in header ascii art
rich_format_help = rich_utils.rich_format_help


def override_help(*args, **kwargs):
    text = Text(art.text2art('TICKERDAX'))
    text.stylize("bold blue")
    print(text)
    rich_format_help(*args, **kwargs)


rich_utils.rich_format_help = override_help

# create cli app
app = typer.Typer(
    pretty_exceptions_show_locals=False
)


# Todo create validate call back for config values from cli
#  https://github.com/TickerDax/tickerdax-client/issues/3
def validate_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if not value:
        raise typer.BadParameter(
            f"You must set this or the environment variable '{param.envvar}'"
        )


rest_api_key_option = typer.Option(
    None,
    callback=validate_callback,
    show_default=False,
    help=Envs.REST_API_KEY.description,
    envvar=Envs.REST_API_KEY.value
)

websocket_api_key_option = typer.Option(
    None,
    callback=validate_callback,
    show_default=False,
    help=Envs.WEBSOCKET_API_KEY.description,
    envvar=Envs.WEBSOCKET_API_KEY.value
)

email_option = typer.Option(
    None,
    callback=validate_callback,
    show_default=False,
    help=Envs.EMAIL.description,
    envvar=Envs.EMAIL.value
)

config_option = typer.Option(
    None,
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    show_default=False,
    help=Envs.CONFIG.description,
    envvar=Envs.CONFIG.value
)

routes_option = typer.Option(
    default=None,
    help="A list of routes to download or stream"
)

symbols_option = typer.Option(
    default=None,
    help="A list of symbols to download or stream"
)

start_option = typer.Option(
    (datetime.now(tz=timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'),
    help="The date and time to start downloading data"
)

end_option = typer.Option(
    datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
    help="The date and time to start downloading data"
)

timeframe_option = typer.Option(
    Default.TIMEFRAME,
    help="The timeframe of the data in the routes"
)

fill_to_now_option = typer.Option(
    True,
    help="Displays debug logs during execution"
)

force_option = typer.Option(
    False,
    help="Forces new REST requests for all missing data, even if that data has already been marked as missing"
)

debug_option = typer.Option(
    False,
    help="Displays debug logs during execution"
)


def get_version():
    """
    Gets the package version.
    """
    project_file_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'pyproject.toml')
    if os.path.exists(project_file_path):
        with open(project_file_path, "rb") as project_file:
            data = tomlkit.load(project_file)
            return data.get('tool', {}).get('poetry', {}).get('version', '0.0.1')
    return importlib.metadata.version(tickerdax.__name__)


def version_callback(value: bool):
    """
    Shows the current cli version

    :param bool value: Whether the version flag was passed.
    """
    if value:
        print(f"TickerDax CLI Version: {get_version()}")
        raise typer.Exit()


@app.callback(no_args_is_help=True)
def callback(version: Optional[bool] = typer.Option(None, "--version", callback=version_callback)):
    """
    The TickerDax CLI tool interfaces with the tickerdax.com REST and websockets APIs. It
    handles common data operations like batch downloading, streaming, and caching data
    locally to minimize network requests.
    """


@app.command()
def create_config(debug: bool = debug_option):
    """
    Creates a new tickerdax config.
    """
    file_formats = [i.value for i in ConfigFormats]
    extension = typer.prompt(
        f'What file format do you want to use? {file_formats}',
        default='yaml'
    )
    if extension not in file_formats:
        raise typer.BadParameter(f'Your choice {extension} is not one of the valid formats {file_formats}')

    # write the example config to the current working directory
    file_path = os.path.join(os.getcwd(), f'config.{extension}')
    with open(file_path, 'w') as config_file:
        if extension == ConfigFormats.YAML.value:
            yaml.dump(EXAMPLE_CONFIG_DATA, config_file)
        elif extension == ConfigFormats.JSON.value:
            json.dump(EXAMPLE_CONFIG_DATA, config_file, indent=2)


@app.command()
def list_routes(debug: bool = debug_option):
    """
    Lists all routes available to download or stream.
    """
    tickerdax_client = TickerDax(
        connect=False,
        debug=debug,
        raise_errors=False
    )
    routes = tickerdax_client.get_available_routes()
    formatting.show_routes(routes)


@app.command()
def download(
        rest_api_key: str = rest_api_key_option,
        route: Annotated[Optional[List[str]], routes_option] = Default.ROUTES,
        symbol: Annotated[Optional[List[str]], symbols_option] = Default.SYMBOLS,
        start: datetime = start_option,
        end: datetime = end_option,
        timeframe: str = timeframe_option,
        config: Optional[Path] = config_option,
        fill_to_now: bool = fill_to_now_option,
        force: bool = force_option,
        debug: bool = debug_option
):
    """
    Downloads data from the routes with the time interval specified in your config.
    """
    Downloader(
        config=config,
        client_kwargs={
            'rest_api_key': rest_api_key,
            'force': force,
            'debug': debug,
            'raise_errors': False
        },
        config_override={
            'routes': {r: symbol for r in route},
            'start': start,
            'end': end,
            'timeframe': timeframe,
            'fill_to_now': fill_to_now
        }
    )


@app.command()
def stream(
        email: str = email_option,
        websocket_api_key: str = websocket_api_key_option,
        rest_api_key: str = rest_api_key_option,
        route: Annotated[Optional[List[str]], routes_option] = Default.ROUTES,
        symbol: Annotated[Optional[List[str]], symbols_option] = Default.SYMBOLS,
        start: datetime = start_option,
        end: datetime = end_option,
        timeframe: str = timeframe_option,
        config: Optional[Path] = config_option,
        fill_to_now: bool = fill_to_now_option,
        force: bool = force_option,
        debug: bool = debug_option
):
    """
    Streams data from the routes specified in your config.
    """
    Streamer(
        config=config,
        client_kwargs={
            'email': email,
            'rest_api_key': rest_api_key,
            'websocket_api_key': websocket_api_key,
            'force': force,
            'debug': debug,
            'raise_errors': False
        },
        config_override={
            'routes': {r: symbol for r in route},
            'start': start,
            'end': end,
            'timeframe': timeframe,
            'fill_to_now': fill_to_now
        }
    )
