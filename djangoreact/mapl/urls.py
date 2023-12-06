from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapl_form, name='mapl'),
]
