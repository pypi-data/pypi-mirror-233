# -*- coding: utf-8 -*-

import click


@click.command()
@click.version_option("1.2.6", prog_name="hello")
@click.option(
    "-n",
    "--name",
    "name",
    type=click.STRING,
    default="World",
    required=False,
    help="The person to greet. Default World",
)
def hello(name: str) -> None:
    """Display Hello!

    Args:
        name (str): name or World by default
    """
    click.echo(f"Hello, {name}!")


if __name__ == "__main__":
    hello()  # pragma: no cover
