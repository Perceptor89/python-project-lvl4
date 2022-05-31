import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView, CreateView

from ..mixins import MyLoginRequiredMixin, MyDeleteView
from ..statuses import consts
from ..statuses.forms import StatusCreateForm
from ..statuses.models import Status


logger = logging.getLogger(__name__)


class StatusListView(MyLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = consts.CONTEXT_OBJECT_NAME


class StatusCreateView(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusCreateForm
    template_name = 'form.html'
    model = Status
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.CREATE_TITLE
        context['btn_name'] = _('Create')
        return context


class StatusUpdateView(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = StatusCreateForm
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.UPDATE_TITLE
        context['btn_name'] = _('Change')
        return context


class StatusDeleteView(MyLoginRequiredMixin, SuccessMessageMixin,
                       MyDeleteView):
    model = Status
    template_name = 'delete_page.html'
    success_message = consts.MESSAGE_DELETE_SUCCESS
    success_url = reverse_lazy(consts.LIST_VIEW)
    constraint_message = consts.MESSAGE_DELETE_CONSTRAINT

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.DELETE_TITLE
        name = self.get_object().get_full_name()
        msg = '{0} {1}?'.format(consts.QUESTION_DELETE, name)
        context['message'] = msg
        return context
