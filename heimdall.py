import click
import subcommands

@click.group()
def cli():
    # click.echo("Hi there")
    ...
    
cli.add_command(subcommands.upload)
cli.add_command(subcommands.download)
cli.add_command(subcommands.list)
cli.add_command(subcommands.delete)