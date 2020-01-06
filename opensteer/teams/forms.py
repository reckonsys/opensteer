# Create the form class.
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from opensteer.teams.models import Team


class TeamForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            Submit('submit', 'Submit')
        )

    class Meta:
        fields = ['name', 'users']
        model = Team
