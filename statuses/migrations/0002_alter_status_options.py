# Generated by Django 4.0.3 on 2022-05-12 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['id'], 'verbose_name_plural': 'Статусы'},
        ),
    ]