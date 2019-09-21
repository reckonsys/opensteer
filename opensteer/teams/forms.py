# Create the form class.
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Field

from opensteer.teams.models import Organization


class OrganizationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            Row(
                Field('timezone', data_live_search="true"),
                Field('standup_hour'),
                Field('standup_minute'),
                css_class='form-row'
            ),
            Row(
                Field('checkin_day'),
                Field('checkin_hour'),
                Field('checkin_minute'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit')
        )

    class Meta:
        model = Organization
        exclude = ['owner']
