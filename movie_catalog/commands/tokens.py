from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens as tokens

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
) -> None:
    """
    Проверяет, существует токен, или нет.
    """
    print(
        f"Токен {token}",
        (
            "[green]существует[/green]."
            if tokens.token_exists(token)
            else "[red]не существует[/red]."
        ),
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    Список всех токенов
    """
    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join(["", *tokens.get_tokens()])))
    print()


@app.command()
def create() -> None:
    """
    Создание нового токена и сохранение его в базу данных
    """
    new_token = tokens.generate_and_save_token()
    print(f"Новый токен [bold][green]{new_token}[/green][/bold] сохранен в базу данных")


@app.command()
def add(token: str) -> None:
    """
    Добавляет токен в БД
    """
    tokens.add_token_in_storage(token)
    print(f"Токен [bold][blue] {token} [/blue][/bold]добавлен в БД")


@app.command(name="rm")
def delete(token: str) -> None:
    """
    Удаление токена из базы данных
    """
    if not tokens.token_exists(token):
        print(f"Токен [bold][red] {token} [/red][/bold] не найден")
        return

    tokens.delete_token(token)
    print(f"Токен [bold][red] {token} [/bold][/red] успешно удален!")
