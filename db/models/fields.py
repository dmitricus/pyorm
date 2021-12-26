class Field:
    def __init__(
            self,
            data_type_field=None,
            verbose_name=None,
            primary_key=False,
            default=None,
            null=True,
    ):
        self.data_type_field = data_type_field
        self.verbose_name = verbose_name
        self.primary_key = self._primary_key(primary_key)
        self.default = default
        self.null = self._null(null)

    @staticmethod
    def _null(null):
        if null:
            return 'NOT NULL'
        return ''

    @staticmethod
    def _primary_key(primary_key):
        if primary_key:
            return ' PRIMARY KEY'
        return ''

    def __str__(self):
        return f'{self.data_type_field}' + self.primary_key


class CharField(Field):
    def __init__(
            self,
            data_type_field='VARCHAR(255)',
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.data_type_field = data_type_field


class IntegerField(Field):
    def __init__(
            self,
            data_type_field='SERIAL',
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.data_type_field = data_type_field


class BooleanField(Field):
    def __init__(
            self,
            data_type_field='BOOLEAN',
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.data_type_field = data_type_field
        self.default = self._default(self.default)

    @staticmethod
    def _default(default):
        if default:
            return 'true'
        return 'false'


class DateTimeField(Field):
    def __init__(
            self,
            data_type_field='timestamp',
            date_time_format="%Y-%m-%dT%H:%M",
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.data_type_field = data_type_field
        self.date_time_format = date_time_format
