from django.urls import path
from . import views
from . import consts


urlpatterns = [
    path('', views.UserListView.as_view(), name=consts.LIST_VIEW),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name=consts.UPDATE_VIEW),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name=consts.DELETE_VIEW),
    path('create/', views.UserCreateView.as_view(), name=consts.CREATE_VIEW)
]

external_patterns = [
    path('login/', views.UserLogin.as_view(), name=consts.LOGIN_VIEW),
    path('logout/', views.UserLogout.as_view(), name=consts.LOGOUT_VIEW),
]
