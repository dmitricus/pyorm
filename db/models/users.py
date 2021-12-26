from db import models
from db.models.base import Model


class AuthUser(Model):
    table_name = 'auth_user'

    id = models.IntegerField(verbose_name='ID')
    name = models.CharField(verbose_name='Имя пользователя')
    birth_date = models.DateTimeField(verbose_name='Дата рождения', date_time_format="%Y-%m-%d")
    gender = models.BooleanField(verbose_name='Пол')

    def __str__(self):
        return f'ID: {self.id} Имя пользователя: {self.name} Дата рождени: {self.birth_date} Пол: {self._gender}'

    @property
    def _gender(self):
        if self.gender:
            return 'Женский'
        return 'Мужской'
