from django.utils.translation import gettext as _


LIST_VIEW = 'labels'
CREATE_VIEW = 'label_create'
UPDATE_VIEW = 'label_update'
DELETE_VIEW = 'label_delete'

LIST_TITLE = _('Labels')
CREATE_TITLE = _('Label creation')
UPDATE_TITLE = _('Label update')
DELETE_TITLE = _('Label delete')
DETAIL_LINK_COLUMN = 2
CREATE_LINK = _('Create label')

CONTEXT_OBJECT_NAME = 'table'
STATUS_OK = 200

TABLE_HEADS = [
    'ID',
    _('Name'),
    _('Creation date'),
]

MESSAGE_CREATE_SUCCESS = _('Label created successfully')
MESSAGE_UPDATE_SUCCESS = _('Label updated successfully')
MESSAGE_DELETE_SUCCESS = _('Label deleted successfully')
QUESTION_DELETE = _('Are you sure you want to delete')
MESSAGE_DELETE_CONSTRAINT = _('Unable to delete label as it is in use')
