from db import models
from db.models.base import Model


class Migration(Model):
    table_name = 'migration'

    id = models.IntegerField(verbose_name='ID')
    name = models.CharField(verbose_name='Имя миграции')
    applied = models.DateTimeField(verbose_name='Дата и время выполнения')
