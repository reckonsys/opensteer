from django.urls import include, path

from opensteer.teams.views import OrganizationEditView, OrganizationDetailView


paths = {
    "organizations": [
        path("new/", view=OrganizationEditView.as_view(), name="new"),
        path("<str:pk>/edit/", view=OrganizationEditView.as_view(), name="edit"),
        path("<str:pk>/", view=OrganizationDetailView.as_view(), name="detail"),
    ],
}


urlpatterns = [
    path(f'{key}/', include((val, key))) for key, val in paths.items()]