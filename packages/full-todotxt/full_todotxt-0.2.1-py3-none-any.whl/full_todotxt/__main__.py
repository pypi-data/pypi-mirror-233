from typing import Optional, List
from pathlib import Path

import click
from pytodotxt.todotxt import TodoTxt, Task  # type: ignore[import]

from .todo import parse_projects, full_backup, locate_todotxt_file, prompt_todo


def run(
    todotxt_file: Optional[Path], add_due: bool, time_format: str, full_screen: bool
) -> None:
    # handle argument
    tfile = locate_todotxt_file(todotxt_file)
    if tfile is None:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    assert tfile is not None

    # read from main todo.txt file
    todos: TodoTxt = TodoTxt(tfile)

    # backup todo.txt file
    full_backup(tfile)

    # list of sources, done.txt will be added if it exists
    todo_sources: List[TodoTxt] = [todos]

    done_file: Path = tfile.parent / "done.txt"
    if not done_file.exists():
        click.secho(
            f"Could not find the done.txt file at {done_file}", err=True, fg="red"
        )
    else:
        todo_sources.append(TodoTxt(done_file))

    for t in todo_sources:
        t.parse()

    # prompt user for new todo
    new_todo: Optional[Task] = prompt_todo(
        add_due=add_due,
        time_format=time_format,
        projects=list(parse_projects(todo_sources)),
        full_screen=full_screen,
    )

    # write back to file
    if new_todo is not None:
        todos.tasks.append(new_todo)
        click.echo(
            "{}: {}".format(click.style("Adding Todo", fg="green"), str(new_todo))
        )
        todos.save(safe=True)


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"], max_content_width=120)
)
@click.argument(
    "TODOTXT_FILE",
    type=click.Path(exists=True, path_type=Path),
    envvar="FULL_TODOTXT_FILE",
    default=None,
    required=False,
)
@click.option(
    "--add-due/--no-add-due",
    is_flag=True,
    default=False,
    help="Add due: key/value flag based on deadline:",
    show_default=True,
)
@click.option(
    "-t",
    "--time-format",
    default="%Y-%m-%dT%H-%M%z",
    envvar="FULL_TODOTXT_TIME_FORMAT",
    show_envvar=True,
    show_default=True,
    help="Specify a different time format for deadline:",
)
@click.option(
    "-f/-p",
    "--full-screen/--prompts",
    "full_screen",
    is_flag=True,
    default=True,
    help="Use prompts or the full screen dialog editor [default: full-screen]",
)
def cli(
    todotxt_file: Optional[Path], full_screen: bool, add_due: bool, time_format: str
) -> None:
    """
    If TODOTXT_FILE is not specified, the environment variable FULL_TODOTXT_FILE will be used.
    """
    run(todotxt_file, add_due, time_format, full_screen=full_screen)


if __name__ == "__main__":
    cli(prog_name="full_todotxt")
