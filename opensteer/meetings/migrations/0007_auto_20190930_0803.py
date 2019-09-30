# Generated by Django 2.2.5 on 2019-09-30 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_auto_20190930_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='teams.Question'),
        ),
        migrations.AlterField(
            model_name='response',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='meetings.Submission'),
        ),
    ]
