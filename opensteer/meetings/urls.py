from django.urls import include, path

from opensteer.meetings.views import SubmissionsView


paths = {
    "submissions": [
        path("<str:submission_id>/", view=SubmissionsView.as_view(), name="detail"),
    ],
}


urlpatterns = [
    path(f'{key}/', include((val, key))) for key, val in paths.items()]
