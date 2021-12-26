import random

import names

from db import migrations, models
from services.util import random_date


def forward():
    models.AuthUser.objects.bulk_create([
        models.AuthUser(
            name=names.get_full_name(),
            birth_date=random_date(1950, 2008).strftime(models.AuthUser.birth_date.date_time_format),
            gender=random.choice([True, False]),
        ) for _ in range(11)
    ])


class Migration(migrations.Migration):
    dependencies = [
        '0002_create_users'
    ]

    operations = [
        migrations.RunPython(forward),
    ]
