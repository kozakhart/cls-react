from django.urls import path
from . import views

urlpatterns = [
    path('', views.opi_form, name='opi_form'),
    path('receipt', views.receipt, name='receipt'),
    path('data', views.index_data, name='index_data'),
    path('thirdyear', views.create_slats, name='create_slats'),
    path('thirdyear/receipt', views.slats_receipt, name='slats_receipt'),
    path('email-confirmation/<str:encoded_string>/', views.email_confirmation, name='email_confirmation'),
    path('certificates', views.certificates, name='certificates'),
    path('certificates/review-certificate/record-id=<str:encoded_string>', views.review_certificate, name='review_certificate'),
    path('mapl', views.mapl_form, name='mapl'),
    #path('test', views.test, name='test'),

]
