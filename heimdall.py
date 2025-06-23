import click
import subcommands
import os, configparser
from pathlib import Path
CONFIG_PATH = os.path.expanduser('~/.config')

@click.group()
@click.pass_context
def cli(ctx:click.Context):
    # click.echo("Hi there")
    # handel file configuration and password management
    path = Path(CONFIG_PATH + "/heimdall_config.ini")
    config = configparser.ConfigParser()
    if not path.is_file():
        config["Encryption"] = {"scheme": "AES", "block-size": 128}
        config["Credentials"] = {}
        config["CloudService"] = {"host": "heimdall.amcsui.ir", "port": "8000"}
        with open(path.as_posix(), "w") as config_file:
            config.write(config_file)            
    config.read(path.as_posix())
    ctx.obj = {"config": config}
    
cli.add_command(subcommands.upload)
cli.add_command(subcommands.download)
cli.add_command(subcommands.list)
cli.add_command(subcommands.delete)