from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_slats, name='create_slats'),
    path('receipt', views.slats_receipt, name='slats_receipt'),
]
