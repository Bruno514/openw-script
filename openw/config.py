import os
import toml
import click

config_dir = os.path.expanduser("~/.config") + "/openw/"
config_file = "config.toml"
defautl_config = """\
[main]
token=""
location=""
units="metric"
"""


def create_config():
    # Create '~/.config/openw' directory
    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)

    if not os.path.isfile(config_dir + config_file):
        with open(config_dir + config_file, "w") as f:
            f.write(defautl_config)

    os.chmod(config_dir + config_file, 0o600)


def get_config():
    with open(config_dir + config_file, "r") as f:
        content = f.read()
        toml_dict = toml.loads(content)

    return toml_dict


def get_config_data(value):
    # Make sure its only readable by the user
    with open(config_dir + config_file, "r") as f:
        content = f.read()
        toml_dict = toml.loads(content)

    return toml_dict["main"][value]


def write_config_data(key, value):
    conf = get_config()
    conf["main"][key] = value
    toml_conf = toml.dumps(conf)
    with open(config_dir + config_file, "w") as f:
        f.write(toml_conf)
