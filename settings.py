import os
from collections import namedtuple
from pathlib import Path

from envparse import env

BASE_DIR = Path(__file__).resolve().parent

env.read_envfile(os.path.join(BASE_DIR, '.env'))

DatabaseSettings = namedtuple('DatabaseSettings', ['database', 'user', 'password', 'host', 'port'])

DATABASE_SETTINGS = DatabaseSettings(
    database=env('POSTGRES_DATABASE', 'users'),
    user=env('POSTGRES_USER', 'pwdusers'),
    password=env('POSTGRES_PASSWORD', 'users'),
    host=env('POSTGRES_HOST', 'postgres'),
    port=env('POSTGRES_PORT', 5432),
)
