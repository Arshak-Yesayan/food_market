# Generated by Django 3.1 on 2020-08-25 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(unique=True)),
                ('password', models.TextField()),
                ('email', models.TextField(unique=True)),
                ('token', models.TextField()),
            ],
        ),
    ]
