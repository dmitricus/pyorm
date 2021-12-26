from __future__ import annotations

from copy import deepcopy

from db.connection import Connection
from db.models.fields import Field


class BaseManager:
    def __init__(self, model_class):
        self.model_class = model_class

    def _execute_query_commit(self, query, params=None):
        with Connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()

    def _execute_query(self, field_names, query, params=None, chunk_size=2000):
        model_objects = list()
        with Connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)

            is_fetching_completed = False
            while not is_fetching_completed:
                result = cursor.fetchmany(size=chunk_size)
                for row_values in result:
                    keys, values = field_names, row_values
                    row_data = dict(zip(keys, values))
                    model_objects.append(self.model_class(**row_data))
                is_fetching_completed = len(result) < chunk_size

        return model_objects

    def get(self, **fields):
        field_names = fields.keys()
        values_field_format = " AND ".join([f'{field}=%s' for field in field_names])
        query = f"SELECT * FROM {self.model_class.table_name} WHERE {values_field_format}"
        params = list()
        for field_name in fields:
            params.append(fields[field_name])
        result = self._execute_query(self.fields, query, params)
        return result[0] if len(result) > 0 else None

    def all(self, ):
        field_names = self.fields.keys()
        fields_format = ', '.join(field_names)
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"
        return self._execute_query(field_names, query)

    def create(self, **fields):
        field_names = fields.keys()
        fields_format = ", ".join(fields.keys())
        values_field_format = ", ".join([f'({", ".join(["%s"] * len(field_names))})'])

        query = f"INSERT INTO {self.model_class.table_name} ({fields_format}) VALUES {values_field_format}"
        params = list()
        for field_name in fields:
            params.append(fields[field_name])
        self._execute_query_commit(query, params)

    def bulk_create(self, rows: list):
        fields = deepcopy(self.fields)
        fields.pop('id')
        field_names = fields.keys()

        fields_format = ", ".join(field_names)
        values_field_format = ", ".join([f'({", ".join(["%s"] * len(field_names))})'] * len(rows))

        query = f"INSERT INTO {self.model_class.table_name} ({fields_format}) VALUES {values_field_format}"
        params = list()
        for row in rows:
            row_values = [row.__dict__[field_name] for field_name in field_names]
            params += row_values
        self._execute_query_commit(query, params)

    def update(self, id, **new_data):
        fields = [value for field_name, value in new_data.items() if field_name != 'id']
        field_names = new_data.keys()
        assert all(field_name in self.fields for field_name in field_names)
        field_format = ', '.join([f'{field_name} = %s' for field_name in field_names if field_name != 'id'])
        query = f"UPDATE {self.model_class.table_name} SET {field_format} WHERE id = %s"
        params = list(fields)
        params.append(id)
        self._execute_query_commit(query, params)

    def delete(self):
        query = f"DELETE FROM {self.model_class.table_name}"
        self._execute_query_commit(query)

    def create_table(self, table_name, fields):
        field_format = ', '.join([f'{field[0]} {field[1]}' for field in fields])
        query = f"CREATE TABLE IF NOT EXISTS {str.lower(table_name)} ({field_format})"
        self._execute_query_commit(query)

    @property
    def fields(self):
        fields_dict = self.model_class.__dict__
        return dict(filter(lambda item: item[1].__class__.__base__ is Field, fields_dict.items()))
