import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import RestrictedError, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.utils.translation import gettext as _

from task_manager.mixins import LoginRequiredMessage
from users import consts
from users.forms import UserCreateForm

logger = logging.getLogger(__name__)


class UserHasPermission(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.id:
            messages.error(self.request, consts.MESSAGE_NO_PERMISSION),
            return redirect(consts.LIST_VIEW)
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    template_name = 'table.html'
    model = User
    context_object_name = consts.CONTEXT_OBJECT_NAME

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.LIST_TITLE
        context['table_heads'] = consts.TABLE_HEADS
        context['update_link'] = consts.UPDATE_VIEW
        context['delete_link'] = consts.DELETE_VIEW
        return context

    def get_queryset(self):
        return User.objects.values_list(
            'id',
            'username',
            Concat(
                'first_name',
                Value(' '),
                'last_name'),
            'date_joined',
            named=True)


class UserUpdateView(LoginRequiredMessage, UserHasPermission,
                     SuccessMessageMixin, UpdateView):
    form_class = UserCreateForm
    model = User
    template_name = 'form.html'
    success_url = reverse_lazy(consts.LIST_VIEW)
    success_message = consts.MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.UPDATE_TITLE
        context['btn_name'] = _("Change")
        return context

    def get_success_url(self):
        logout(self.request)
        return super().get_success_url()


class UserDeleteView(LoginRequiredMessage, UserHasPermission,
                     SuccessMessageMixin, DeleteView):
    model = User
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


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = consts.MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.CREATE_TITLE
        context['btn_name'] = _('Register user')
        return context


class UserLogin(LoginView):
    template_name = 'form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = consts.LOGIN_TITLE
        context['btn_name'] = _('Enter')
        return context

    def get_success_url(self):
        messages.success(self.request, consts.MESSAGE_LOGIN_SUCCESS)
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, consts.MESSAGE_INVALID_PASSWORD)
        return super().form_invalid(form)


class UserLogout(LoginRequiredMessage, LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, consts.MESSAGE_LOGOUT_SUCCESS)
        return super().dispatch(request, *args, **kwargs)
