from django.urls import path

from tasks import consts, views


urlpatterns = [
    path('', views.TaskListView.as_view(), name=consts.LIST_VIEW),
    path('create/', views.TaskCreateView.as_view(), name=consts.CREATE_VIEW),
    path('<int:pk>/', views.TaskDetailView.as_view(), name=consts.DETAIL_VIEW),
    path(
        '<int:pk>/update/',
        views.TaskUpdateView.as_view(),
        name=consts.UPDATE_VIEW,
    ),
    path(
        '<int:pk>/delete/',
        views.TaskDeleteView.as_view(),
        name=consts.DELETE_VIEW,
    )
]
