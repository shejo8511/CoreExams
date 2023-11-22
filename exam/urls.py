from django.urls import path, include
from exam import views
from user import views as userViews

urlpatterns = [
    path('', include('user.urls')),
    path('home/', userViews.home, name='home'),
    path('reports/reportExam01/', views.ReportExam01.as_view(), name='reportExam01'),
    path('guardar-captura/', views.guardar_captura, name='guardar-captura'),
    #path('guardar-select-diagnostic/', views.guardar_select_diagnostic, name='guardar-select-diagnostic'),
    #path('stream/download-pdf/', views.download_pdf, name='download-pdf'),
    #path('stream/pdf/',views.generate_pdf,name='generate_pdf'),
    #path('stream/record_diagnostic/',views.record_diagnostic,name='record_diagnostic'),
    path('stream/videoStream/',views.videoStream,name="videoStream"),
    path('abrir_pdf/<int:exam_id>/', views.abrir_pdf, name='abrir_pdf'),
    path('type_exam/list_type_exam/', views.listTypeExam, name='list_type_exam'),
    path('type_exam/type_exam/', views.typeExam, name='type_exam'),
    path('reports/examsSelect/', views.examsSelect, name='examsSelect'),
    #path('reports/examsSelect/', views.saveExams, name='saveExams'),
    path('cancel/', views.cancel, name='cancel'),
]