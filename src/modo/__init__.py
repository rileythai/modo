import click


@click.group()
def cli():
    pass


@cli.command()
def hello():
    click.echo("Hello world")


cli.add_command(hello)
