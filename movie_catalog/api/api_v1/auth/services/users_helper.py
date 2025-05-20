from abc import (
    ABC,
    abstractmethod,
)


class AbstractUsersHelper(ABC):
    @abstractmethod
    def get_password_user(
        self,
        username: str,
    ) -> str | None:
        """
        Проверяет есть ли в БД пароль, под полученным username
        Если есть, возвращает True, если нет, то False

        :param username: - имя пользователя
        :return: - пароль, если он есть, либо None
        """

    @classmethod
    def check_password_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Проверяет соответствие переданного пароля, паролю,
        находящемуся в БД, под переданным username

        :param username: имя пользователя
        :param password: пароль
        :return: True если валидация прошла успешно и False, в ином случае
        """
        db_password = self.get_password_user(username=username)
        if db_password is None:
            return False
        return self.check_password_match(
            password1=db_password,
            password2=password,
        )
