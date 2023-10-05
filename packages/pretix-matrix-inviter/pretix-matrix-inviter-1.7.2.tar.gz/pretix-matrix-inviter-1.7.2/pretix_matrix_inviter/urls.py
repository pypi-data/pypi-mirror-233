from django.urls import path

from .views import MatrixInviterSettingsView

urlpatterns = [
    path(
        "control/event/<str:organizer>/<str:event>/matrix_inviter/",
        MatrixInviterSettingsView.as_view(),
        name="settings",
    )
]
