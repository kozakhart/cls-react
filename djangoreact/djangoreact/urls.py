"""
URL configuration for djangoreact project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .custom_admin_auth import custom_admin_login, custom_admin_logout

urlpatterns = [
    path('admin/login/', custom_admin_login, name='admin_login'),
    path('admin/logout/', custom_admin_logout, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('myapp.urls')),
]
#admin.site.login = path('cls/', custom_admin_login)
