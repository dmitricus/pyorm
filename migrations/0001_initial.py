from db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        '0001_initial'
    ]

    operations = [
        migrations.CreateModel(
            name='migration',
            fields=[
                ('id', models.IntegerField(verbose_name='ID')),
                ('name', models.CharField(verbose_name='Имя миграции')),
                ('applied', models.DateTimeField(verbose_name='Дата и время выполнения')),
            ],
        ),
        migrations.CreateModel(
            name='auth_user',
            fields=[
                ('id', models.IntegerField(verbose_name='ID')),
                ('name', models.CharField(verbose_name='Имя пользователя')),
                ('birth_name', models.DateTimeField(verbose_name='Дата рождения')),
                ('gender', models.BooleanField(verbose_name='Пол')),
            ],
        ),
    ]
