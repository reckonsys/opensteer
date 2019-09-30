# Generated by Django 2.2.5 on 2019-09-26 04:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_team_staffs'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('meetings', '0002_auto_20190924_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('meeting_id', models.UUIDField()),
                ('meeting_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Member')),
            ],
            options={
                'unique_together': {('member', 'meeting_type', 'meeting_id')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='standupresponse',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='standupresponse',
            name='member',
        ),
        migrations.RemoveField(
            model_name='standupresponse',
            name='question',
        ),
        migrations.RemoveField(
            model_name='standupresponse',
            name='standup',
        ),
        migrations.DeleteModel(
            name='CheckinResponse',
        ),
        migrations.DeleteModel(
            name='StandupResponse',
        ),
        migrations.AddField(
            model_name='response',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Submission'),
        ),
        migrations.AlterUniqueTogether(
            name='response',
            unique_together={('question', 'submission')},
        ),
    ]
