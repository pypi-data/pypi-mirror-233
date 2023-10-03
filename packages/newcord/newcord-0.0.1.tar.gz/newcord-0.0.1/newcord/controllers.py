from __future__ import annotations

import shutil
import typer

from typing import TYPE_CHECKING, Any, Sequence
from newcord.helpers import get_success_message, build_requirements, confirm
from pip import main
from pipenv.cli import cli

if TYPE_CHECKING:
    from newcord.context import Context


__all__: Sequence[str] = ("init_command_controller",)


def init_command_controller(ctx: Context) -> Any:
    dependencies_installed = False
    ctx.project_location.mkdir(exist_ok=True)

    # Add the base files to the new project
    shutil.copytree(ctx.base, ctx.project_location, dirs_exist_ok=True)

    # Create the /bot folder in the project directory and add the bot files
    bot_dir = ctx.project_location / "bot"
    bot_dir.mkdir(exist_ok=True)
    shutil.copytree(ctx.bot_path, bot_dir, dirs_exist_ok=True)

    # Creating the requirements.txt file
    with open(ctx.project_location / "requirements.txt", "w") as f:
        f.write(build_requirements("mongodb"))

    # Ask to install dependencies
    if confirm("Would you like to install the required dependencies"):
        s1 = typer.style(
            text="Installing dependencies from", fg="bright_white", bold=True
        )
        s2 = typer.style(
            text=f"{ctx.project_location / 'requirements.txt'}",
            fg="bright_cyan",
            bold=True,
            underline=True,
        )
        typer.echo(f"{s1} {s2}")
        try:
            main(["install", "-r", f"{ctx.project_location / 'requirements.txt'}"])
            dependencies_installed = True
        except:
            pass

    typer.echo(
        get_success_message(
            ctx.project_location, dependencies_installed=dependencies_installed
        )
    )
