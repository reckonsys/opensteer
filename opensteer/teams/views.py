from django.views import View
from django.shortcuts import render, redirect

from opensteer.teams.forms import OrganizationForm
from opensteer.teams.models import Organization


class OrganizationEditView(View):
    form_class = OrganizationForm
    template_name = 'teams/organization_form.html'

    def get(self, request, pk=None):
        organization = None
        if pk is not None:
            organization = Organization.objects.get(pk=pk)
        form = self.form_class(instance=organization)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk=None):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        if pk is not None:
            organization = form.save()
            return redirect('organizations:detail', pk=organization.id)
        organization = form.save(commit=False)
        organization.owner = request.user
        organization.save()
        return redirect('organizations:detail', pk=organization.id)


class OrganizationDetailView(View):
    template_name = 'teams/organization_detail.html'

    def get(self, request, pk):
        organization = Organization.objects.get(pk=pk)
        return render(
            request, self.template_name, {'organization': organization})
