from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _

import django_filters
from django_filters import filters

from ..labels.models import Label
from ..statuses.models import Status
from ..tasks.models import Task
from ..users.models import User


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        ex_choices = [('', '-------------')] + list(
            User.objects.values_list(
                'id',
                Concat('first_name', Value(' '), 'last_name'),
                named=True,
            ).all()
        )
        self.fields['executor'].choices = ex_choices
        self.fields['labels'].required = False

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels'),
        }


class TaskFilter(django_filters.FilterSet):
    statuse_all = Status.objects.values_list('id', 'name', named=True).all()
    status = filters.ChoiceFilter(label=_('Status'), choices=statuse_all)
    user_all = User.objects.values_list(
        'id', Concat('first_name', Value(' '), 'last_name'), named=True
    ).all()
    executor = filters.ChoiceFilter(label=_('Executor'), choices=user_all)
    label_all = Label.objects.values_list('id', 'name', named=True)
    labels = filters.ChoiceFilter(label=_('Label'), choices=label_all)
    self_task = filters.BooleanFilter(
        label=_('Only my tasks'),
        widget=forms.CheckboxInput,
        method='filter_self',
        field_name='self_task',
    )

    def filter_self(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            queryset = queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
