from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from opensteer.teams.models import Team
from opensteer.teams.forms import TeamForm


class TeamFormView(LoginRequiredMixin, View):
    form_class = TeamForm
    template_name = 'teams/team_form.html'

    def get(self, request, team_id=None):
        if team_id is None:
            # Create team form
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        # Edit team form
        team = Team.objects.get(id=team_id)
        form = self.form_class(instance=team)
        return render(request, self.template_name, {'form': form})

    def post(self, request, team_id=None):
        if team_id is None:
            # Create team
            form = self.form_class(request.POST)
            if not form.is_valid():
                return render(request, self.template_name, {'form': form})
            team = form.save(commit=False)
            return redirect('teams:detail', team_id=team.id)
        # Edit Team
        team = Team.objects.get(id=team_id)
        form = self.form_class(request.POST, instance=team)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        form.save()
        return redirect('teams:detail', team_id=team.id)


class TeamDetailView(View):
    template_name = 'teams/team_detail.html'

    def get(self, request, team_id):
        team = Team.objects.get(id=team_id)
        return render(
            request, self.template_name, {'team': team})
