from django.urls import path
from company import views

urlpatterns =[
    path('membership/membership/', views.membership, name='membership'),
    path('membership/list_membership/', views.listMembership, name='list_membership'),
    path('exams/list_exams/', views.listExams, name='list_exams'),
    path('company_edit/<int:company_id>/', views.company_edit, name='company_edit'),
]
