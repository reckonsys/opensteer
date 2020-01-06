from django.urls import include, path

from opensteer.teams.views import TeamFormView, TeamDetailView


paths = {
    "teams": [
        path("new/", view=TeamFormView.as_view(), name="new"),
        path("<str:team_id>/edit/", view=TeamFormView.as_view(), name="edit"),
        path("<str:team_id>/", view=TeamDetailView.as_view(), name="detail"),
    ],
}


urlpatterns = [
    path(f'{key}/', include((val, key))) for key, val in paths.items()]
