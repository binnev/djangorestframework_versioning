# Generated by Django 4.0.5 on 2022-09-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_thing_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='status',
            field=models.CharField(choices=[('OK', 'Ok'), ('NOT_OK', 'Not Ok')], default='OK', max_length=20),
        ),
    ]
