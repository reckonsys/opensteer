from django.views import View
from django.shortcuts import render, redirect

from opensteer.teams.forms import OrganizationForm
from opensteer.teams.models import Organization


class OrganizationEditView(View):
    form_class = OrganizationForm
    template_name = 'teams/organization_form.html'

    def get(self, request, id=None):
        if id is None:
            # Create organization form
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        # Edit organization form
        organization = Organization.objects.get(id=id)
        organization.utc_to_local()
        form = self.form_class(instance=organization)
        return render(request, self.template_name, {'form': form})

    def post(self, request, id=None):
        if id is None:
            # Create Organization
            form = self.form_class(request.POST)
            if not form.is_valid():
                return render(request, self.template_name, {'form': form})
            organization = form.save(commit=False)
            organization.local_to_utc()
            organization.owner = request.user
            organization.save()
            return redirect('organizations:detail', id=organization.id)
        # Edit Organization
        organization = Organization.objects.get(id=id)
        form = self.form_class(request.POST, instance=organization)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        organization.local_to_utc()
        organization.save()
        return redirect('organizations:detail', id=organization.id)


class OrganizationDetailView(View):
    template_name = 'teams/organization_detail.html'

    def get(self, request, id):
        organization = Organization.objects.get(id=id)
        return render(
            request, self.template_name, {'organization': organization})
