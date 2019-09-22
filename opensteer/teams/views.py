from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from opensteer.teams.models import Organization, Team
from opensteer.teams.forms import OrganizationForm, TeamForm


class OrganizationFormView(LoginRequiredMixin, View):
    form_class = OrganizationForm
    template_name = 'teams/organization_form.html'

    def get(self, request, organization_id=None):
        if organization_id is None:
            # Create organization form
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        # Edit organization form
        organization = Organization.objects.get(id=organization_id)
        organization.utc_to_local()
        form = self.form_class(instance=organization)
        return render(request, self.template_name, {'form': form})

    def post(self, request, organization_id=None):
        if organization_id is None:
            # Create Organization
            form = self.form_class(request.POST)
            if not form.is_valid():
                return render(request, self.template_name, {'form': form})
            organization = form.save(commit=False)
            organization.local_to_utc()
            organization.owner = request.user
            organization.save()
            return redirect(
                'organizations:detail', organization_id=organization.id)
        # Edit Organization
        organization = Organization.objects.get(id=organization_id)
        form = self.form_class(request.POST, instance=organization)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        organization.local_to_utc()
        organization.save()
        return redirect(
            'organizations:detail', organization_id=organization.id)


class OrganizationDetailView(View):
    template_name = 'teams/organization_detail.html'

    def get(self, request, organization_id):
        organization = Organization.objects.get(id=organization_id)
        return render(
            request, self.template_name, {'organization': organization})


class TeamFormView(LoginRequiredMixin, View):
    form_class = TeamForm
    template_name = 'teams/team_form.html'

    def get(self, request, organization_id=None, team_id=None):
        if team_id is None:
            # Create team form
            form = self.form_class()
            organization = Organization.objects.get(id=organization_id)
            return render(request, self.template_name, {
                'form': form, 'organization': organization})
        # Edit team form
        team = Team.objects.get(id=team_id)
        form = self.form_class(instance=team)
        return render(request, self.template_name, {
            'form': form, 'organization': team.organization})

    def post(self, request, organization_id=None, team_id=None):
        if team_id is None:
            # Create team
            form = self.form_class(request.POST)
            if not form.is_valid():
                return render(request, self.template_name, {'form': form})
            team = form.save(commit=False)
            organization = Organization.objects.get(id=organization_id)
            team.organization = organization
            team.save()
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
