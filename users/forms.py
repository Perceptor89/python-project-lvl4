import logging

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
