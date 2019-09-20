# Generated by Django 2.2.5 on 2019-09-20 09:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_remove_team_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='checkin_day',
            field=models.PositiveSmallIntegerField(choices=[(5, 'Friday'), (1, 'Monday'), (6, 'Saturday'), (0, 'Sunday'), (4, 'Thursday'), (2, 'Tuesday'), (3, 'Wednesday')], default=4, validators=[django.core.validators.MaxValueValidator(6)]),
        ),
    ]
