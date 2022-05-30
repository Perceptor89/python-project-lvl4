"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .users.urls import urlpatterns as users_views
from .users.urls import external_patterns as login_logout
from .statuses.urls import urlpatterns as statuses_views
from .tasks.urls import urlpatterns as tasks_views
from .labels.urls import urlpatterns as labels_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', include(login_logout)),
    path('users/', include(users_views)),
    path('statuses/', include(statuses_views)),
    path('tasks/', include(tasks_views)),
    path('labels/', include(labels_views)),
]
