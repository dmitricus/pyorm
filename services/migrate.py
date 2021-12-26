import pkgutil
import sys
from datetime import datetime
from importlib import import_module, reload

import psycopg2

from db import models

MIGRATIONS_MODULE_NAME = 'migrations'


class MigrateDB:
    def __init__(self):
        self.disk_migrations = {}
        self.migrated = self._migrated()

    def run(self):
        was_loaded = MIGRATIONS_MODULE_NAME in sys.modules
        module = import_module(MIGRATIONS_MODULE_NAME)

        if was_loaded:
            reload(module)

        migration_names = {
            name for _, name, is_pkg in pkgutil.iter_modules(module.__path__)
            if not is_pkg and name[0] not in '_~'
        }
        for migration_name in migration_names:
            if migration_name in self.migrated:
                continue
            migration_path = '%s.%s' % (MIGRATIONS_MODULE_NAME, migration_name)
            migration_module = import_module(migration_path)
            self.disk_migrations[migration_name] = migration_module.Migration(
                migration_name,
            )
        self.migrate()
        return self.disk_migrations

    def migrate(self):
        print('Running migrations:')
        if not self.disk_migrations:
            print('  No migrations to apply.')
        for migration_name, migration in self.disk_migrations.items():
            for operation in migration.operations:
                operation.database_forwards()
            self.migration_complete(migration_name, migration)

    def migration_complete(self, migration_name, migration):
        migration.objects.create(
            name=migration_name,
            applied=datetime.strftime(datetime.now(), migration.applied.date_time_format),
        )
        print(f'  {migration_name}')

    def _migrated(self):
        try:
            return (x.name for x in models.Migration.objects.all())
        except psycopg2.DatabaseError:
            return ()
