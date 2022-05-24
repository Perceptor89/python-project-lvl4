from django.urls import path

from labels import consts, views


urlpatterns = [
    path('', views.LabelListView.as_view(), name=consts.LIST_VIEW),
    path('create/', views.LabelCreateView.as_view(), name=consts.CREATE_VIEW),
    path(
        '<int:pk>/update/',
        views.LabelUpdateView.as_view(),
        name=consts.UPDATE_VIEW,
    ),
    path(
        '<int:pk>/delete/',
        views.LabelDeleteView.as_view(),
        name=consts.DELETE_VIEW,
    )
]
