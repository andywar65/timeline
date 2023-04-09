# from django.contrib import messages
# from django.http import Http404
# from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now

# from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, RedirectView

from timeline.models import Phase, get_month_dict
from timeline.views.phase import HxPageTemplateMixin

# CreateView,
# DetailView,
# TemplateView,
# UpdateView,
# from timeline.forms import PhaseCreateForm


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
