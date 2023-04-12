from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView, RedirectView, TemplateView

from timeline.forms import ProjectCreateForm
from timeline.models import Phase, get_month_dict, get_position_by_parent
from timeline.views.phase import HxOnlyTemplateMixin, HxPageTemplateMixin


class BaseRedirectView(RedirectView):
    """Redirects to now()"""

    def get_redirect_url(self):
        return reverse(
            "timeline:project_list", kwargs={"year": now().year, "month": now().month}
        )


class ProjectListView(PermissionRequiredMixin, HxPageTemplateMixin, ListView):
    """Rendered in #content"""

    permission_required = "timeline.view_phase"
    model = Phase
    template_name = "timeline/project/htmx/list.html"

    def get_queryset(self):
        qs = Phase.objects.filter(parent_id=None)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["year"] = self.kwargs["year"]
        context["month"] = self.kwargs["month"]
        context["month_dict"] = get_month_dict(context["year"], context["month"])
        return context


class ProjectCreateView(HxOnlyTemplateMixin, FormView):
    """Rendered in #add_button, swaps none"""

    permission_required = "timeline.add_phase"
    model = Phase
    form_class = ProjectCreateForm
    template_name = "timeline/project/htmx/create.html"

    def form_valid(self, form):
        project = Phase()
        project.title = form.cleaned_data["title"]
        project.start = form.cleaned_data["start"]
        project.position = get_position_by_parent(None)
        project.save()
        report = _("Added project '%(title)s'") % {"title": project.title}
        messages.success(self.request, report)
        if form.cleaned_data["suite"]:
            project.create_suite()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("timeline:refresh_list")


class ProjectAddButtonView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #add_button"""

    template_name = "timeline/project/htmx/add_button.html"
