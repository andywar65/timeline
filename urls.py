from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views.phase import (
    PhaseAddButtonView,
    PhaseCreateView,
    PhaseDeleteView,
    PhaseDetailView,
    PhaseListView,
    PhaseMoveDownView,
    PhaseMoveUpView,
    PhaseUpdateView,
    RefreshListView,
)
from .views.project import (
    BaseRedirectView,
    ProjectAddButtonView,
    ProjectCreateView,
    ProjectListView,
)

app_name = "timeline"
urlpatterns = [
    # Generic urlpatterns
    path(
        "refresh/list/",
        RefreshListView.as_view(),
        name="refresh_list",
    ),
    # Project urlpatterns
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
        "project/create/",
        ProjectCreateView.as_view(),
        name="project_create",
    ),
    path(
        "project/add/button/",
        ProjectAddButtonView.as_view(),
        name="project_add_button",
    ),
    # Phase urlpatterns
    path(
        _("project/<pk>/<int:year>/<int:month>/"),
        PhaseListView.as_view(),
        name="list",
    ),
    path(
        "project/<pk>/phase/create/",
        PhaseCreateView.as_view(),
        name="create",
    ),
    path(
        "project/<pk>/add/button/",
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
