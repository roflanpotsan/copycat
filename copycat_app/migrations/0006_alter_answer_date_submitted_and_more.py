# Generated by Django 4.2.7 on 2023-12-06 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copycat_app', '0005_alter_answerrating_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 6, 14, 42, 6, 709789)),
        ),
        migrations.AlterField(
            model_name='question',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 6, 14, 42, 6, 709230)),
        ),
    ]
