from django.utils.translation import gettext as _


LIST_VIEW = 'list'
UPDATE_VIEW = 'user_update'
DELETE_VIEW = 'user_delete'
CREATE_VIEW = 'user_create'
LOGIN_VIEW = 'login'
LOGOUT_VIEW = 'logout'

UPDATE_TITLE = _('Change user')
DELETE_TITLE = _('Delete user')
CREATE_TITLE = _('User registration')
LOGIN_TITLE = _('Authorization')

CONTEXT_OBJECT_NAME = 'users'
STATUS_OK = 200

QUESTION_DELETE = _('Are you sure want to delete')
MESSAGE_LOGIN_SUCCESS = _('Successful login')
MESSAGE_INVALID_PASSWORD = _('Invalid pair user-password')
MESSAGE_NO_PERMISSION = _('You have no permission to edit '
                          'another user\'s profile')
MESSAGE_UPDATE_SUCCESS = _('User changed successfully')
MESSAGE_DELETE_SUCCESS = _('User was successfully deleted')
MESSAGE_DELETE_CONSTRAINT = _('Unable to delete user as it is in use')
MESSAGE_CREATE_SUCCESS = _('User successfully created')
MESSAGE_LOGOUT_SUCCESS = _('You are logged out')
