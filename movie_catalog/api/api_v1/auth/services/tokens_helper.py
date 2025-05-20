import secrets
from abc import (
    ABC,
    abstractmethod,
)


class AbstractTokensHelper(ABC):
    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Проверяет - существует ли токен

        :param token: str
        :return: bool
        """

    @abstractmethod
    def add_token_in_storage(
        self,
        token: str,
    ) -> None:
        """
        Добавляет токен в хранилище

        :param token: str
        :return: None
        """

    @classmethod
    def generate_token(cls) -> str:
        """
        Генерирует токен

        :return: str
        """
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token_in_storage(token=token)
        return token
