import typer
from rich.prompt import Prompt

import uva.commands as commands
import uva.helpers as helpers

app = typer.Typer()


@app.command()
def login(
        username: str = typer.Argument(
            None,
            show_default=False,
            help="Your uva username"
        ),
        password: str = typer.Argument(
            None,
            show_default=False,
            help="Your uva password"
        )
):
    """
        Logs you into the uva portal
    """
    if username is None:
        username = Prompt.ask("Enter your name :sunglasses:")

    if password is None:
        password = Prompt.ask("Enter your uva password", password=True)
    commands.login(username, password)


@app.command()
def logout():
    commands.logout()


@app.command()
def submit(
        problem_id: int = typer.Argument(
            ...,
            show_default=False,
            help="Uva problem id"
        ),
        filepath: str = typer.Argument(
            ...,
            show_default=False,
            help="Path to the solution file"
        ),
        language: helpers.SubmitLanguage = typer.Argument(
            None,
            show_default=False,
            help="Submission language"
        )
):
    if language is None:
        language = helpers.detect_language(filepath)

    if language is None:
        ask_user = Prompt.ask("Please enter submit language", choices=['c', 'java', 'c++', 'pascal', 'c++11', 'python'])
        language = helpers.SubmitLanguage(ask_user)
    elif language is helpers.SubmitLanguage.cplusplus:
        ask_user = Prompt.ask("Please enter c++ version", choices=['c++', 'c++11'], default='c++')
        language = helpers.SubmitLanguage(ask_user)
    commands.submit(problem_id, filepath, int(language))


@app.command()
def latest_subs(count: int = typer.Argument(
        10,
        min=0,
        max=100,
        help='Number of submissions to get'
    )
):
    commands.get_latest_subs(count)


@app.command()
def pdf(problem_id: int = typer.Argument(
    ...,
    show_default=False,
    help="Uva problem id"
)
):
    commands.get_pdf_file(str(problem_id))


# @app.command()
# def test(subid: str):
#     console = Console(log_time=False, log_path=False)
#     commands.wait_for_submission_results(subid, console)


if __name__ == "__main__":
    app()
