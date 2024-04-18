from django.urls import path, include
from . import views
urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-session/', views.verify_session, name='verify-session'),

    path('', views.apiOverview, name="api-overview"),
    path('student-list/', views.student_list, name="student-list"),
    path('filemaker/', views.filemaker_view, name='filemaker'),
    path('lti/', views.lti_view, name='lti'),
    path('get-certificate-data/', views.get_certificate_data, name='get-certificate-data'),
    path('award-certificate/', views.award_certificate, name='award-certificate'),
    path('example-lti/', views.example_lti_view, name='example_lti_view'),
    path('update/<str:student>/', views.student_update, name='student-update'),
    path('delete/<str:student>/', views.student_delete, name='student-delete'),
    path('get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    path('logout/', views.logout_view, name='logout'),
    path('need-approval-filemaker/', views.need_approval_filemaker, name='need-approval-filemaker'),
    path('get-user-info/', views.get_user_info, name='get-user-info'),
    path('get-grades/', views.get_student_grades, name='get-grades'),
    path('edit-record/', views.edit_records, name='edit-record'),
    path('qualtrics-report/', views.qualtrics_reports, name='qualtrics-reports'),
    path('laser-database/', views.laser_data, name='laser-data'),
    path('get-db-schema/', views.get_db_schema, name='get-db-schema'),
]