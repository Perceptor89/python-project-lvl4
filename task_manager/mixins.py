import logging

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import DeleteView


logger = logging.getLogger(__name__)

MESSAGE_LOGIN_REQUIRED = _('You have no authorization! Log in please.')


class LoginRequiredMessage(AccessMixin):
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, MESSAGE_LOGIN_REQUIRED),
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class MyDeleteView(DeleteView):
    constraint_message = ''

    def form_valid(self, form):
        try:
            self.object.delete()
        except RestrictedError:
            messages.error(self.request, self.constraint_message)
        else:
            messages.success(self.request, self.success_message)
        return redirect(self.success_url)
