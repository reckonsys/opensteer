# Generated by Django 2.2.5 on 2019-09-21 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokers', '0002_auto_20190916_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poker',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokers', to='teams.Member'),
        ),
        migrations.AlterField(
            model_name='poker',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokers', to='teams.Team'),
        ),
    ]