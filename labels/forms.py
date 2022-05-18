from django import forms
from django.utils.translation import gettext as _

from labels.models import Label


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']
        labels = {'name': _('Name')}
