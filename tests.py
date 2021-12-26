from unittest import TestCase, mock

from db import models, connection
from services import migrate
from services.util import random_date


@mock.patch('db.connection.psycopg2')
class TestMain(TestCase):

    def db_conn(self, mock_sql):
        self.assertIs(connection.psycopg2, mock_sql)
        conn = mock.Mock()
        mock_sql.connect.return_value = conn

        cursor = mock.MagicMock()
        mock_result = mock.MagicMock()

        cursor.__enter__.return_value = mock_result
        cursor.__exit___ = mock.MagicMock()

        conn.cursor.return_value = cursor

        connection.Connection()

        return cursor

    @mock.patch('builtins.print')
    def test_db_migration(self, mock_print, mock_sql):
        mock_cursor = self.db_conn(mock_sql)
        migrated_db = migrate.MigrateDB().run()
        mock_cursor.execute.assert_called()
        self.assertEqual(len(mock_cursor.method_calls), 7)

        self.assertTupleEqual(tuple(migrated_db.keys()), tuple({'0001_initial', '0002_create_users'}))

    def test_db_create(self, mock_sql):
        mock_cursor = self.db_conn(mock_sql)
        birth_date_random = random_date(1950, 2008).strftime(models.AuthUser.birth_date.date_time_format)
        models.AuthUser.objects.create(
            name='Иванова Анна Ивановна',
            birth_date=birth_date_random,
            gender=True,
        )
        self.assertEqual(len(mock_cursor.method_calls), 1)
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called()
        mock_cursor.execute.assert_called_once_with(
            'INSERT INTO auth_user (name, birth_date, gender) VALUES (%s, %s, %s)',
            ['Иванова Анна Ивановна', birth_date_random, True]
        )

    def test_db_bulk_create(self, mock_sql):
        mock_cursor = self.db_conn(mock_sql)
        models.AuthUser.objects.bulk_create(
            [
                models.AuthUser(
                    name='Tami Kelley',
                    birth_date='2007-08-06',
                    gender=False,
                ),
                models.AuthUser(
                    name='Sandra Rzeszutko',
                    birth_date='1988-01-27',
                    gender=True,
                ),
                models.AuthUser(
                    name='Gloria Cormier',
                    birth_date='1961-01-29',
                    gender=True,
                ),
            ]
        )
        self.assertEqual(len(mock_cursor.method_calls), 1)
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called()
        mock_cursor.execute.assert_called_once_with(
            'INSERT INTO auth_user (name, birth_date, gender) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)',
            [
                'Tami Kelley',
                '2007-08-06',
                False,
                'Sandra Rzeszutko',
                '1988-01-27',
                True,
                'Gloria Cormier',
                '1961-01-29',
                True,
            ]
        )

    def test_db_get(self, mock_sql):
        mock_cursor = self.db_conn(mock_sql)
        models.AuthUser.objects.get(name='Иванова Анна Ивановна', gender=True)
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called()
        mock_cursor.execute.assert_called_once_with(
            'SELECT * FROM auth_user WHERE name=%s AND gender=%s',
            ['Иванова Анна Ивановна', True]
        )

    def test_db_update(self, mock_sql):
        mock_cursor = self.db_conn(mock_sql)
        models.AuthUser.objects.update(
            id=1,
            name='Петров Петр Петрович',
            birth_date='1988-01-27',
            gender=False,
        )
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called()
        mock_cursor.execute.assert_called_once_with(
            'UPDATE auth_user SET name = %s, birth_date = %s, gender = %s WHERE id = %s',
            ['Петров Петр Петрович', '1988-01-27', False, 1]
        )
