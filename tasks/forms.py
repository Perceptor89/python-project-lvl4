from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _

from labels.models import Label
from statuses.models import Status

from tasks.models import Task
import tasks.consts



class TaskForm(forms.ModelForm):

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
