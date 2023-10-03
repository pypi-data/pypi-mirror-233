from __future__ import annotations

import os
import typer
import questionary

from pathlib import Path
from questionary import Style
from typing import Any, Literal, Sequence

__all__: Sequence[str] = (
    "style",
    "get_success_message",
    "get_template_dir",
    "select_from_directory",
    "ask_question",
    "confirm",
    "create_project_path",
    "build_requirements",
)


# fmt: off
style = Style([
    ('qmark', 'fg:#00ffff bold'),       # token in front of the question
    ('question', 'white bold'),               # question text
    ('answer', 'fg:black'),      # submitted answer text behind the question
    ('pointer', 'fg:#00ffff bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#00ffff bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
# fmt: on


def get_success_message(bot_dir: Path, dependencies_installed: bool) -> str:
    want_navigation = Path(os.curdir).resolve() != bot_dir.resolve()

    def style_message(
        msg: Any,
        color: str = "bright_white",
        is_bold: bool = True,
        underline: bool = False,
    ):
        return typer.style(text=msg, fg=color, bold=is_bold, underline=underline)

    steps = [
        f"{style_message('Start your bot:')} {style_message('python bot/bot.py', 'bright_cyan')}\n",
        f"{style_message('Discord.py docs:')} {style_message('https://discordpy.readthedocs.io/en/stable/', 'bright_cyan')}\n",
    ]

    if want_navigation:
        steps.insert(
            0,
            f"{style_message('Navigate to your project directory:')} {style_message(f'cd {bot_dir}', 'bright_cyan')}\n",
        )

    if not dependencies_installed:
        steps.insert(
            1 if want_navigation else 0,
            f"{style_message('Install dependencies:')} {style_message(f'pip install -r requirements.txt', 'bright_cyan')}\n",
        )

    return f"""
{style_message("Successfully created your new project!")}

{style_message("Next Steps:", underline=True)}
{"".join(f"{style_message(count)}: {step}" for count, step in enumerate(steps, start=1))}
"""


def get_template_dir() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")


def select_from_directory(prompt: str, directory: str):
    return (
        questionary.select(
            message=prompt,
            choices=list(
                i.capitalize()
                for i in filter(lambda x: not x.startswith("_"), os.listdir(directory))
            ),
            style=style,
            pointer="❯",
        )
        .unsafe_ask()
        .lower()
    )


def ask_question(prompt: str, default: str = ""):

    return questionary.text(message=f"{prompt} ›", default=default, style=style).unsafe_ask()


def confirm(prompt: str, default: bool = True):
    return questionary.confirm(message=prompt, default=default, style=style).ask()


def create_project_path() -> Path:
    return Path(ask_question("Where would you like to create your project", "./"))


def build_requirements(database: Literal["mongodb", "no-database"]) -> str:
    requirements = ["discord.py[speed]"]

    if database == "mongodb":
        requirements.append("beanie")
        requirements.append("pymongo[srv]")

    text_req = "\n".join(requirements)
    text_dev_req = "\n".join(["black", "mypy"])
    return f"""{text_req}

# For Devlopment
{text_dev_req}
"""
