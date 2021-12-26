import psycopg2

from settings import DATABASE_SETTINGS


class Connection(object):
    def __init__(self):
        self.db_setting = DATABASE_SETTINGS
        self._db_name = self.db_setting.database
        self._db_user = self.db_setting.user
        self._db_password = self.db_setting.password
        self._db_host = self.db_setting.host
        self._db_port = self.db_setting.port

    def __enter__(self):
        self._conn = psycopg2.connect(
            database=self._db_name,
            user=self._db_user,
            password=self._db_password,
            host=self._db_host,
            port=self._db_port,
        )
        self._conn.set_isolation_level(0)
        return self._conn

    def get_cursor(self):
        return self._conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self._conn.rollback()
            self._conn.close()
            raise
        self._conn.close()
