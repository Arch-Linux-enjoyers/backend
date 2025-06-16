class PasswordsDontMatchError(ValueError):

    def __init__(self) -> None:
        super().__init__('Пароли не совпадают')


class InvalidLoginOrPasswordError(ValueError):

    def __init__(self) -> None:
        super().__init__('Неверное имя пользователя/email или пароль')


class UserAccountDeactivatedError(ValueError):

    def __init__(self) -> None:
        super().__init__('Аккаунт пользователя отключен')


class UsernameOrPasswordDontProvidedError(ValueError):

    def __init__(self) -> None:
        super().__init__('Необходимо указать имя пользователя и пароль')

