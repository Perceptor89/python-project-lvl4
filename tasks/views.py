from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Value, RestrictedError
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (DetailView, ListView,
                                  CreateView, DeleteView, UpdateView)

from task_manager.mixins import LoginRequiredMessage
from tasks import consts
from tasks.forms import TaskForm, TaskFilter
from tasks.models import Task


class TaskListView(LoginRequiredMessage, ListView):
    template_name = 'tasks/table.html'
    model = Task
    context_object_name = consts.CONTEXT_OBJECT_NAME

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.LIST_TITLE
        context['table_heads'] = consts.TABLE_HEADS
        context['create_path_name'] = consts.CREATE_LINK
        context['create_path'] = consts.CREATE_VIEW
        context['update_link'] = consts.UPDATE_VIEW
        context['delete_link'] = consts.DELETE_VIEW
        context['detail_col'] = consts.DETAIL_LINK_COLUMN
        context['detail_path'] = consts.DETAIL_VIEW
        context['filter'] = TaskFilter(self.request.GET,
                                       request=self.request,
                                       queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        return Task.objects.values_list('id', 'name', 'status__name',
                                        Concat('author__first_name',
                                               Value(' '),
                                               'author__last_name'),
                                        Concat('executor__first_name',
                                               Value(' '),
                                               'executor__last_name'),
                                        'created_at',
                                        named=True)


class TaskCreateView(LoginRequiredMessage, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'form.html'
    model = Task
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.CREATE_TITLE
        context['btn_name'] = _('Create')
        return context

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMessage, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.UPDATE_TITLE
        context['btn_name'] = _('Change')
        return context


class TaskDeleteView(LoginRequiredMessage, DeleteView):
    template_name = 'delete_page.html'
    model = Task
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_DELETE_SUCCESS

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

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id:
            if self.get_object().author != self.request.user:
                messages.error(self.request, consts.MESSAGE_DELETE_CONSTRAINT)
                return redirect(consts.LIST_VIEW)
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMessage, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.DETAIL_TITLE
        context['update_link'] = consts.UPDATE_VIEW
        context['delete_link'] = consts.DELETE_VIEW
        return context
