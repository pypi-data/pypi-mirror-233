#!/usr/bin/env python3

import os
import re

from datetime import datetime, date
from typing import Union, List, Optional, Set
from pathlib import Path
from shutil import copyfile

import click
import dateparser
from pytodotxt.todotxt import TodoTxt, Task  # type: ignore[import]

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, input_dialog, button_dialog
from prompt_toolkit.document import Document
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.formatted_text import HTML

PathIsh = Union[Path, str]


class ProjectTagValidator(Validator):
    def validate(self, document: Document) -> None:
        text = document.text

        if len(text.strip()) == 0:
            raise ValidationError(message="You must specify at least one project tag")

        # check if all input matches '+projectag'
        for project_tag in text.split():
            if not bool(re.match(r"\+\w+", project_tag)):
                raise ValidationError(
                    message=f"'{project_tag}' doesn't look like a project tag. e.g. '+home'"
                )


# prompt the user to add a todo
def prompt_todo(
    *, add_due: bool, time_format: str, projects: List[str], full_screen: bool = True
) -> Optional[Task]:
    # prompt the user for a new todo (just the text)
    todo_text: Optional[str] = None
    if full_screen:
        todo_text = input_dialog(title="Add Todo:").run()
    else:
        todo_text = prompt("[Todo]> ")

    if not todo_text:
        return None
    elif not todo_text.strip():
        if full_screen:
            message_dialog(title="Error", text="No input provided for the todo").run()
        else:
            click.echo("No input provided for the todo", err=True)
        return None

    projects_raw: str = ""
    # if you provided a project in the text itself, skip forcing you to specify one
    if len(Task(todo_text).projects) == 0:
        # project tags
        click.echo("Enter one or more tags, hit 'Tab' to autocomplete")
        projects_raw = prompt(
            "[Enter Project Tags]> ",
            completer=FuzzyWordCompleter(projects),
            complete_while_typing=True,
            validator=ProjectTagValidator(),
            bottom_toolbar=HTML("<b>Todo:</b> {}".format(todo_text)),
        )

    # select priority
    if full_screen:
        todo_priority: str = button_dialog(
            title="Priority:",
            text="A is highest, C is lowest",
            buttons=[
                ("A", "A"),
                ("B", "B"),
                ("C", "C"),
            ],
        ).run()
    else:

        def prompt_priority() -> Optional[str]:
            click.echo("Enter a priority: (A, B, or C): ", nl=False)
            prio: str = click.getchar().upper()
            click.echo()
            if prio not in ["A", "B", "C"]:
                click.echo(f"Invalid priority '{prio}'")
                return None
            return prio

        resp: Optional[str] = None
        while resp not in ["A", "B", "C"]:
            resp = prompt_priority()
        assert resp in ["A", "B", "C"]
        todo_priority = resp

    # ask if the user wants to add a time
    if full_screen:
        add_time: bool = button_dialog(
            title="Deadline:",
            text="Do you want to add a deadline for this todo?",
            buttons=[
                ("No", False),
                ("Yes", True),
            ],
        ).run()
    else:
        add_time = click.confirm(
            "Do you want to add a deadline for this todo?", default=True
        )

    # prompt for adding a deadline
    todo_time: Optional[datetime] = None
    if add_time:
        while todo_time is None:
            if full_screen:
                todo_time_str: Optional[str] = input_dialog(
                    title="Describe the deadline.",
                    text="For example:\n'9AM', 'noon', 'tomorrow at 10PM', 'may 30th at 8PM'",
                ).run()
                # if user hit cancel
                if todo_time_str is None:
                    add_time = False
                    break
                else:
                    todo_time = dateparser.parse(
                        todo_time_str, settings={"PREFER_DATES_FROM": "future"}
                    )
                    if todo_time is None:
                        message_dialog(
                            title="Error",
                            text="Could not parse '{}' into datetime".format(
                                todo_time_str
                            ),
                        ).run()
            else:
                from autotui.options import Option, options
                from autotui.prompts import prompt_datetime

                with options(Option.LIVE_DATETIME):
                    todo_time = prompt_datetime(prompt_msg="[Deadline]> ")

    if todo_time is not None:
        # floor the time to the nearest minute
        todo_time = todo_time.replace(second=0, microsecond=0)

        # if the user didn't specify a timezone, assume they meant their local timezone
        if todo_time.tzinfo is None:
            todo_time = todo_time.replace(tzinfo=datetime.now().astimezone().tzinfo)

    # construct the Task
    constructed: str = f"({todo_priority})"
    constructed += f" {date.today()}"
    constructed += f" {todo_text}"
    if projects_raw.strip():
        constructed += f" {projects_raw}"
    if todo_time is not None:
        constructed += f" deadline:{datetime.strftime(todo_time, time_format)}"
        if add_due:
            constructed += f" due:{datetime.strftime(todo_time, r'%Y-%m-%d')}"

    t = Task(constructed)
    return t


def full_backup(todotxt_file: PathIsh) -> None:
    """
    Backs up the todo.txt file before writing to it
    """
    backup_file: PathIsh = f"{todotxt_file}.full.bak"
    copyfile(str(todotxt_file), str(backup_file))


def parse_projects(todo_sources: List[TodoTxt]) -> Set[str]:
    """Get a list of all tags from the todos"""
    projects = set()
    for tf in todo_sources:
        for todo in tf.tasks:
            for proj in todo.projects:
                projects.add(f"+{proj}")
    return projects


def locate_todotxt_file(todotxt_filepath: Optional[Path]) -> Optional[Path]:
    if todotxt_filepath is not None:
        if not os.path.exists(todotxt_filepath):
            click.echo(
                f"The provided file '{todotxt_filepath}' does not exist.", err=True
            )
            return None
        else:
            return todotxt_filepath
    else:  # no todo file passed, test some common locations
        home = Path.home()
        possible_locations = [
            home / ".config/todo/todo.txt",
            home / ".todo/todo.txt",
            home / ".todo.txt",
            home / "todo.txt",
        ]
        if "XDG_CONFIG_HOME" in os.environ:
            possible_locations.insert(
                0, Path(os.environ["XDG_CONFIG_HOME"]) / "todo/todo.txt"
            )
        if "TODO_DIR" in os.environ:
            possible_locations.insert(0, Path(os.environ["TODO_DIR"]) / "todo.txt")
        for p in possible_locations:
            if p.exists():
                click.echo(f"Found todo.txt file at {p}, using...")
                return p
        else:
            return None
