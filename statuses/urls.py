from django.urls import path

from statuses import consts, views


urlpatterns = [
    path('', views.StatusListView.as_view(), name=consts.LIST_VIEW),
    path('create/', views.StatusCreateView.as_view(), name=consts.CREATE_VIEW),
    path(
        '<int:pk>/update/',
        views.StatusUpdateView.as_view(),
        name=consts.UPDATE_VIEW
    ),
    path(
        '<int:pk>/delete/',
        views.StatusDeleteView.as_view(),
        name=consts.DELETE_VIEW,
    )
]
