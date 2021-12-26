from db import models

MIGRATIONS_MODULE_NAME = 'migrations'


class Migration:
    from db.managers import base
    manager_class = base.BaseManager
    table_name = 'migration'

    id = models.IntegerField(verbose_name='ID')
    name = models.CharField(verbose_name='Имя миграции')
    applied = models.DateTimeField(verbose_name='Дата и время выполнения')

    operations = []
    dependencies = []

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.operations = list(self.__class__.operations)
        self.dependencies = list(self.__class__.dependencies)


class ModelOperation:
    def __init__(self, name):
        self.name = name


class CreateModel(ModelOperation):
    from db.managers import base
    manager_class = base.BaseManager

    def __init__(self, fields, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = fields

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()

    def database_forwards(self):
        self.objects.create_table(self.name, self.fields)


class RunPython:

    def __init__(self, code):
        if not callable(code):
            raise ValueError("RunPython must be supplied with a callable")
        self.code = code

    def database_forwards(self):
        self.code()
