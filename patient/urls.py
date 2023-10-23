from django.urls import path
from patient import views

urlpatterns = [
    path('list_patients/', views.listPatientExam, name='list_patients'),
]