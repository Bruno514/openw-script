import click
import requests

def valid_token(token):
    param = {"appid": token}
    r = requests.get("http://api.openweathermap.org/data/2.5/weather", param)
    if r.status_code == 401:
        raise click.UsageError("Not a valid API key.")


def valid_location(location, token):
    # Check if location is valid
    parameters = {"q": location, "appid": token}
    r = requests.get("http://api.openweathermap.org/data/2.5/weather", params=parameters)
    is_valid_location = r.status_code != 404

    if not is_valid_location:
        raise click.UsageError("Not a valid location.")

