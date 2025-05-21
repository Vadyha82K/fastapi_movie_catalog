from fastapi import FastAPI

from api.api_v1.movies.crud import storage


async def lifespan(app: FastAPI):
    # Действие до запуска приложения
    # ставим эту функцию на паузу на время работы приложения
    yield
    # выполняем завершение работы,
    # закрываем соединение, финально сохраняем файлы
