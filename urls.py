from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    BaseRedirectView,
    PhaseAddButtonView,
    PhaseCreateView,
    PhaseDeleteView,
    PhaseDetailView,
    PhaseListView,
    PhaseMoveDownView,
    PhaseMoveUpView,
    PhaseUpdateView,
    ProjectListView,
)

app_name = "timeline"
urlpatterns = [
    path(
        "",
        BaseRedirectView.as_view(),
        name="base",
    ),
    path(
        _("project/list/<int:year>/<int:month>/"),
        ProjectListView.as_view(),
        name="project_list",
    ),
    path(
        "<int:year>/<int:month>/",
        PhaseListView.as_view(),
        name="list",
    ),
    path(
        "phase/create/",
        PhaseCreateView.as_view(),
        name="create",
    ),
    path(
        "phase/add/button/",
        PhaseAddButtonView.as_view(),
        name="add_button",
    ),
    path(
        "phase/<pk>/",
        PhaseDetailView.as_view(),
        name="detail",
    ),
    path(
        "phase/<pk>/update/",
        PhaseUpdateView.as_view(),
        name="update",
    ),
    path(
        "phase/<pk>/delete/",
        PhaseDeleteView.as_view(),
        name="delete",
    ),
    path(
        "phase/<pk>/move/down/",
        PhaseMoveDownView.as_view(),
        name="move_down",
    ),
    path(
        "phase/<pk>/move/up/",
        PhaseMoveUpView.as_view(),
        name="move_up",
    ),
]
