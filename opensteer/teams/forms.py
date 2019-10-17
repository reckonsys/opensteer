# Create the form class.
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Field

# from opensteer.teams.models import Organization, Team
from opensteer.teams.models import Team


class OrganizationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            Row(
                Field('timezone', data_live_search="true"),
                Field('meeting_hour'),
                Field('meeting_minute'),
                Field('checkin_day'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit')
        )

    class Meta:
        # model = Organization
        exclude = ['owner']


class TeamForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            Submit('submit', 'Submit')
        )

    class Meta:
        model = Team
        exclude = ['organization']
