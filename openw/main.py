import click
import requests
import toml
import os

from openw.config import create_config, get_config_data, write_config_data
from openw.validate import valid_token, valid_location

create_config()

# Temp symbols
temp_sym = {"metric": "ºC", "imperial": "ºF", "standard": "ºK"}


@click.command()
@click.option(
    "--token",
    type=str,
    default=get_config_data("token"),
    help="Your API key from openweathermap.org",
)
@click.option(
    "--location",
    type=str,
    default=get_config_data("location"),
    help="Location to fetch the weather from",
)
@click.option(
    "--units",
    type=click.Choice(["metric", "imperial", "standard"], case_sensitive=False),
    default=get_config_data("units"),
    help="Choose metric, imperial or standard.",
)
def cli(token, location, units):
    if not token:
        token = click.prompt("Enter your token")
        click.echo()
        write_config_data("token", token)

    if not location:
        location = click.prompt("Enter the location")
        click.echo()

    if not units:
        click.echo("metric, imperial, standard")
        units = click.prompt("Choose a unit: ")
        click.echo()
        if units not in temp_sym.keys():
            write_config_data("units", units)
        else:
            raise click.UsageError(f"'{units.title()} is not a valid unit'")

    if units not in temp_sym.keys():
        raise click.UsageError(f"'{units.title()} is not a valid unit'")

    # Token and location validation
    valid_token(token)
    valid_location(location, token)

    # Load parameters
    parameters = {"q": location, "appid": token, "units": units}

    # Get the JSON from openweathermap.org
    json = requests.get(
        "http://api.openweathermap.org/data/2.5/weather", parameters
    ).json()
    country = json["sys"]["country"]
    weather = json["weather"][0]
    main = json["main"]
    wind = json["wind"]
    coord = json["coord"]

    click.echo(f"{location}, {country}")
    click.echo(
        f"{click.style('Description', fg='green')}: {weather['description'].capitalize()}"
    )
    click.echo()
    click.echo(
        f"{click.style('Temperature', fg='blue')}: {main['temp']} {temp_sym[units]}. Feels like {main['feels_like']} {temp_sym[units]}."
    )
    click.echo(f"{click.style('Pressure', fg='blue')}: {main['pressure']}hPa")
    click.echo(f"{click.style('Humidity', fg='blue')}: {main['humidity']}%")
    click.echo(f"{click.style('Wind Speed', fg='blue')}: {wind['speed']} m/s")
    click.echo()
    click.echo(
        f"{click.style('Coordinates', fg='red')}: {coord['lon']}, {coord['lat']}"
    )


if __name__ == "__main__":
    cli()
