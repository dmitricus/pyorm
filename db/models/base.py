from db.managers.base import BaseManager


class ModelBase(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class Model(metaclass=ModelBase):
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        return '<%s (%s)>' % (self.__class__.__name__, self.pk)

    def __str__(self):
        return f'{self.__class__.__name__} object ({self.pk})'

    @property
    def pk(self):
        return self.id
