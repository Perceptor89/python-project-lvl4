import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.translation import gettext as _

from ..mixins import LoginRequiredMessage, MyDeleteView
from ..labels import consts
from ..labels.forms import LabelForm
from ..labels.models import Label

logger = logging.getLogger(__name__)


class LabelListView(LoginRequiredMessage, ListView):
    template_name = 'table.html'
    context_object_name = consts.CONTEXT_OBJECT_NAME

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.LIST_TITLE
        context['table_heads'] = consts.TABLE_HEADS
        context['create_path_name'] = consts.CREATE_LINK
        context['create_path'] = consts.CREATE_VIEW
        context['update_link'] = consts.UPDATE_VIEW
        context['delete_link'] = consts.DELETE_VIEW
        return context

    def get_queryset(self):
        return Label.objects.values_list('id', 'name',
                                         'created_at',
                                         named=True)


class LabelCreateView(LoginRequiredMessage, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'form.html'
    model = Label
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.CREATE_TITLE
        context['btn_name'] = _('Create')
        return context


class LabelUpdateView(LoginRequiredMessage, SuccessMessageMixin, UpdateView):
    form_class = LabelForm
    template_name = 'form.html'
    model = Label
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.UPDATE_TITLE
        context['btn_name'] = _('Change')
        return context


class LabelDeleteView(LoginRequiredMessage, MyDeleteView):
    template_name = 'delete_page.html'
    model = Label
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_DELETE_SUCCESS
    constraint_message = consts.MESSAGE_DELETE_CONSTRAINT

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.DELETE_TITLE
        context['btn_name'] = _('Yes, delete')
        name = self.get_object().get_full_name()
        msg = '{0} {1}?'.format(consts.QUESTION_DELETE, name)
        context['message'] = msg
        return context
