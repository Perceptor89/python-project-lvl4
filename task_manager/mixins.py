from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


MESSAGE_LOGIN_REQUIRED = _('You have no authorization! Log in please.')


class LoginRequiredMessage(AccessMixin):
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, MESSAGE_LOGIN_REQUIRED),
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
