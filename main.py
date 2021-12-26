from functools import wraps

from db import models
from services import migrate
from services.util import random_date


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        sharp = "#" * len(func_name)
        print(f'### {func_name} ###')
        result = func(*args, **kwargs)
        print(f'### {sharp} ###')
        return result

    return wrapper


@decorator
def start_migrate():
    migrate.MigrateDB().run()


@decorator
def select_all():
    auth_users = models.AuthUser.objects.all()
    for user in auth_users:
        print(user)


def create_user():
    models.AuthUser.objects.create(
        name='Иванова Анна Ивановна',
        birth_date=random_date(1950, 2008).strftime(models.AuthUser.birth_date.date_time_format),
        gender=True,
    )


@decorator
def get_ivanova():
    auth_user_ivanova = models.AuthUser.objects.get(name='Иванова Анна Ивановна', gender=True)
    print(str(auth_user_ivanova))
    return auth_user_ivanova


@decorator
def get_petrov():
    auth_user_petrov = models.AuthUser.objects.get(name='Петров Петр Петрович', gender=False)
    print(str(auth_user_petrov))
    return auth_user_petrov


@decorator
def update_user(auth_user_ivanova):
    models.AuthUser.objects.update(
        id=auth_user_ivanova.pk,
        name='Петров Петр Петрович',
        birth_date=random_date(1950, 2008).strftime(models.AuthUser.birth_date.date_time_format),
        gender=False,
    )


def main():
    # Выполянем миграции
    start_migrate()
    # Выводим всех пользователей
    select_all()
    # Создаем одного пользователя
    create_user()
    # Получим пользователя иванова
    auth_user_ivanova = get_ivanova()
    # Изменяем пользователя иванова на петров
    update_user(auth_user_ivanova)
    # Смотрим на изменения
    get_petrov()
    # Еще раз запросим всех пользователей
    select_all()


if __name__ == '__main__':
    main()
