from django.urls import include, path

from opensteer.teams.views import OrganizationFormView, OrganizationDetailView


paths = {
    "organizations": [
        path("new/", view=OrganizationFormView.as_view(), name="new"),
        path("<str:id>/edit/", view=OrganizationFormView.as_view(), name="edit"),
        path("<str:id>/", view=OrganizationDetailView.as_view(), name="detail"),
    ],
}


urlpatterns = [
    path(f'{key}/', include((val, key))) for key, val in paths.items()]
