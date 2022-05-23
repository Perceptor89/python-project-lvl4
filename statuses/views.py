import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from task_manager.mixins import LoginRequiredMessage
from statuses import consts
from statuses.forms import StatusCreateForm
from statuses.models import Status

logger = logging.getLogger(__name__)


class StatusListView(LoginRequiredMessage, ListView):
    template_name = 'table.html'
    model = Status
    context_object_name = consts.CONTEXT_OBJECT_NAME

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.LIST_TITLE
        context['table_heads'] = consts.TABLE_HEADS
        context['create_path_name'] = _('Create status')
        context['create_path'] = consts.CREATE_VIEW
        context['update_link'] = consts.UPDATE_VIEW
        context['delete_link'] = consts.DELETE_VIEW
        return context

    def get_queryset(self):
        return Status.objects.values_list(
            'id', 'name', 'created_at', named=True
        )


class StatusCreateView(LoginRequiredMessage, SuccessMessageMixin, CreateView):
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


class StatusUpdateView(LoginRequiredMessage, SuccessMessageMixin, UpdateView):
    form_class = StatusCreateForm
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.UPDATE_TITLE
        context['btn_name'] = _("Change")
        return context


class StatusDeleteView(LoginRequiredMessage, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'delete_page.html'
    success_message = consts.MESSAGE_DELETE_SUCCESS
    success_url = reverse_lazy(consts.LIST_VIEW)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.DELETE_TITLE
        context['btn_name'] = _('Yes, delete')
        name = self.get_object().get_full_name()
        msg = '{0} {1}?'.format(consts.QUESTION_DELETE, name)
        context['message'] = msg
        return context

    def form_valid(self, form):
        try:
            self.object.delete()
        except RestrictedError:
            msg = consts.MESSAGE_DELETE_CONSTRAINT
            messages.error(self.request, msg)
        else:
            messages.success(self.request, self.success_message)
        return redirect(self.success_url)
