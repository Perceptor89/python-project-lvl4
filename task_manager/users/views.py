import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.utils.translation import gettext as _

from ..mixins import MyLoginRequiredMixin, MyDeleteView
from ..users import consts
from ..users.forms import UserCreateForm
from ..users.models import User

logger = logging.getLogger(__name__)


class UserPermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.id:
            messages.error(self.request, consts.MESSAGE_NO_PERMISSION),
            return redirect(consts.LIST_VIEW)
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    template_name = 'users/users_list.html'
    model = User
    context_object_name = consts.CONTEXT_OBJECT_NAME


class UserUpdateView(MyLoginRequiredMixin, UserPermissionMixin,
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


class UserDeleteView(MyLoginRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, MyDeleteView):
    model = User
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


class UserLogout(MyLoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, consts.MESSAGE_LOGOUT_SUCCESS)
        return super().dispatch(request, *args, **kwargs)
