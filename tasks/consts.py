from django.utils.translation import gettext as _


LIST_VIEW = 'tasks'
CREATE_VIEW = 'task_create'
UPDATE_VIEW = 'task_update'
DELETE_VIEW = 'task_delete'
DETAIL_VIEW = 'task_detail'

LIST_TITLE = _('Tasks')
CREATE_TITLE = _('Task creation')
UPDATE_TITLE = _('Task update')
DELETE_TITLE = _('Task delete')
DETAIL_TITLE = _('Task view')
DETAIL_LINK_COLUMN = 2
CREATE_LINK = _('Create task')

TASKS_MODEL_VAR = 'tasks'
STATUS_OK = 200

TABLE_HEADS = [
    'ID',
    _('Name'),
    _('Status'),
    _('Author'),
    _('Executor'),
    _('Creation date'),
]

LOGIN_PAGE = '/login/'

MESSAGE_CREATE_SUCCESS = _('Task created successfully')
MESSAGE_UPDATE_SUCCESS = _('Task updated successfully')
MESSAGE_DELETE_SUCCESS = _('Task deleted successfully')
QUESTION_DELETE = _('Are you sure you want to delete')
MESSAGE_DELETE_CONSTRAINT = _('The task may be deleted only by author')