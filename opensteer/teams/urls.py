from django.urls import include, path

from opensteer.teams.views import (
    OrganizationFormView, OrganizationDetailView, TeamFormView, TeamDetailView)


paths = {
    "organizations": [
        path("new/", view=OrganizationFormView.as_view(), name="new"),
        path("<str:organization_id>/edit/", view=OrganizationFormView.as_view(), name="edit"),
        path("<str:organization_id>/", view=OrganizationDetailView.as_view(), name="detail"),
    ],
    "teams": [
        path("new/<str:organization_id>/", view=TeamFormView.as_view(), name="new"),
        path("<str:team_id>/edit/", view=TeamFormView.as_view(), name="edit"),
        path("<str:team_id>/", view=TeamDetailView.as_view(), name="detail"),
    ],
}


urlpatterns = [
    path(f'{key}/', include((val, key))) for key, val in paths.items()]
