from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from tree_queries.forms import TreeNodeChoiceField

from .models import Phase


class PhaseCreateForm(ModelForm):
    parent = TreeNodeChoiceField(queryset=Phase.objects.all(), required=False)

    class Meta:
        model = Phase
        exclude = ("position",)


class ProjectCreateForm(ModelForm):
    suite = forms.BooleanField(initial=False, label=_("Create suite"), required=False)

    class Meta:
        model = Phase
        fields = ("title", "start")
