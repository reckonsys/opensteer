# Generated by Django 2.2.5 on 2019-09-24 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20190924_0412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='checkin_hour',
            new_name='meeting_hour',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='checkin_minute',
            new_name='meeting_minute',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='standup_hour',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='standup_minute',
        ),
    ]
