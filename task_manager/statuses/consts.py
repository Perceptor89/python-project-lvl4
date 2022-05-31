from django.utils.translation import gettext as _


LIST_VIEW = 'statuses'
CREATE_VIEW = 'status_create'
UPDATE_VIEW = 'status_update'
DELETE_VIEW = 'status_delete'

CREATE_TITLE = _('Status creation')
UPDATE_TITLE = _('Status update')
DELETE_TITLE = _('Status delete')

CONTEXT_OBJECT_NAME = 'statuses'
STATUS_OK = 200

MESSAGE_CREATE_SUCCESS = _('Status created successfully')
MESSAGE_UPDATE_SUCCESS = _('Status updated successfully')
MESSAGE_DELETE_SUCCESS = _('Status deleted successfully')
QUESTION_DELETE = _('Are you sure you want to delete')
MESSAGE_DELETE_CONSTRAINT = _('Unable to delete status as it is in use')
