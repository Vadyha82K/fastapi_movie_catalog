from typing import Annotated

import typer
from rich import print

from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="token",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Tokens management.",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
):
    """
    Проверяет, существует токен, или нет.
    """
    print(
        f"Токен {token}",
        (
            "[green]существует[/green]."
            if redis_tokens.token_exists(token)
            else "[red]не существует[/red]."
        ),
    )
