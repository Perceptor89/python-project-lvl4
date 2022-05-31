from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (DetailView, CreateView, UpdateView)
from django_filters.views import FilterView

from ..mixins import MyLoginRequiredMixin, MyDeleteView
from ..users.models import User
from ..tasks import consts
from ..tasks.forms import TaskForm, TaskFilter
from ..tasks.models import Task


class TaskListView(MyLoginRequiredMixin, FilterView):
    template_name = 'tasks/tasks_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = consts.CONTEXT_OBJECT_NAME


class TaskCreateView(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
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


class TaskUpdateView(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
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


class TaskDeleteView(MyLoginRequiredMixin, MyDeleteView):
    template_name = 'delete_page.html'
    model = Task
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_DELETE_SUCCESS
    constraint_message = consts.MESSAGE_DELETE_CONSTRAINT

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.DELETE_TITLE
        name = self.get_object().get_full_name()
        msg = '{0} {1}?'.format(consts.QUESTION_DELETE, name)
        context['message'] = msg
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id:
            if self.get_object().author != self.request.user:
                messages.error(self.request, consts.MESSAGE_DELETE_CONSTRAINT)
                return redirect(consts.LIST_VIEW)
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(MyLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
