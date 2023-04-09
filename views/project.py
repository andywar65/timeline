from django.contrib import messages

# from django.http import Http404
# from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, RedirectView, TemplateView

#
# DetailView,
# ,
# UpdateView,
from timeline.forms import ProjectCreateForm
from timeline.models import Phase, get_month_dict, get_position_by_parent
from timeline.views.phase import HxOnlyTemplateMixin, HxPageTemplateMixin


class BaseRedirectView(RedirectView):
    """Redirects to now()"""

    def get_redirect_url(self):
        return reverse(
            "timeline:project_list", kwargs={"year": now().year, "month": now().month}
        )


class ProjectListView(HxPageTemplateMixin, ListView):
    """Rendered in #content"""

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


class ProjectCreateView(HxOnlyTemplateMixin, CreateView):
    """Rendered in and redirects to #add_button"""

    model = Phase
    form_class = ProjectCreateForm
    template_name = "timeline/project/htmx/create.html"

    def form_valid(self, form):
        form.instance.position = get_position_by_parent(None)
        report = _("Added project '%(title)s'") % {"title": form.instance.title}
        messages.success(self.request, report)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("timeline:project_add_button") + "?refresh=true"


class ProjectAddButtonView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #add_button, may trigger refresh list"""

    template_name = "timeline/project/htmx/add_button.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if "refresh" in request.GET:
            response["HX-Trigger-After-Swap"] = "refreshList"
        return response
