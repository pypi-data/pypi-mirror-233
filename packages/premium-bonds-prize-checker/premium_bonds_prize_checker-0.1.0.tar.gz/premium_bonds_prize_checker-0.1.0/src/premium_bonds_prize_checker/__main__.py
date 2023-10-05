import json
import os
from importlib.metadata import PackageNotFoundError, version
from typing import Optional

import httpx
import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing_extensions import Annotated

app = typer.Typer()

try:
    __version__ = version("premium-bonds-prize-checker")
except PackageNotFoundError:
    __version__ = "dev"


def version_callback(value: bool):
    if value:
        print(__version__)
        raise typer.Exit()


def read_config_file():
    try:
        with open(os.path.expanduser("~/.config/premium-bonds/config.json")) as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return None


def get_and_print_results(holders_number):
    console = Console()
    text = Text()
    table = Table(title="Winning Bonds")
    resp = httpx.post(
        "https://www.nsandi.com/premium-bonds-have-i-won-ajax",
        data={"field_premium_bond_period": "this_month", "field_premium_bond_number": holders_number},
    )
    resp.raise_for_status()
    result = resp.json()
    if result["status"] == "win":
        text.append(result["header"], style="bold green")
        text.append("\n")
        text.append(result["tagline"], style="green")
        text.append("\n")
        table.add_column("Prize")
        table.add_column("Bond #")
        for winner in result["history"]:
            table.add_row(winner["prize"], winner["bond_number"])
    else:
        text.append("No win this month 😭", style="red")
    console.print(text)
    if table:
        console.print(table)


@app.command()
def main(
    holders_number: Annotated[Optional[str], typer.Argument()] = None,
    _: Optional[bool] = typer.Option(None, "-v", "--version", callback=version_callback, is_eager=True),
):
    config = read_config_file()
    if not holders_number and not config:
        print("No holders number specified and no config found")
        raise typer.Abort(1)
    if holders_number:
        if "," in holders_number:
            numbers = holders_number.split(",")
            for number in numbers:
                print(number)
                get_and_print_results(number)
        else:
            get_and_print_results(holders_number)
    else:
        for name, number in config.items():
            print(name)
            get_and_print_results(number)


if __name__ == "__main__":
    app()
