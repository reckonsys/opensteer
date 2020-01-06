from opensteer.teams.models import Member
from django.db.models.signals import post_save
from opensteer.meetings.choices import SubmissionStatus
from opensteer.meetings.models import Standup, Checkin, Submission


def member_updated(sender, instance, created, **kwargs):
    if not created:
        return
    member = instance
    for standup in Standup.objects.filter(team=member.team, is_active=True):
        member.submissions.create(meeting=standup)
    for checkin in Checkin.objects.filter(team=member.team, is_active=True):
        member.submissions.create(meeting=checkin)
    print('create_submission', sender, member, created)


def meeting_updated(sender, instance, created, **kwargs):
    if not created:
        return
    for member in instance.team.members.all():
        member.submissions.create(meeting=instance)


def submission_updated(sender, instance, created, **kwargs):
    if created:
        return
    meeting = instance.meeting
    if Submission.objects.filter(meeting_id=meeting.id, status=SubmissionStatus.OPEN).exists():
        # Some submissions are still open
        return
    # TODO: send an email to managers / admin when all members respond
    meeting.deactivate()


post_save.connect(member_updated, sender=Member)
post_save.connect(meeting_updated, sender=Standup)
post_save.connect(meeting_updated, sender=Checkin)
post_save.connect(submission_updated, sender=Submission)
