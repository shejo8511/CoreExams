from django.urls import path
from company import views

urlpatterns =[
    path('membership/membership/', views.membership, name='membership'),
    path('membership/list_membership/', views.listMembership, name='list_membership'),
    path('exams/list_exams/', views.listExams, name='list_exams'),
    path('company/company_edit/<int:company_id>/', views.company_edit, name='company_edit'),
    path('location/country/country/', views.country, name='country'),
    path('location/country/list_country/', views.listCountry, name='list_country'),
    path('location/province/province/', views.province, name='province'),
    path('location/province/list_province/', views.listProvince, name='list_province'),
    path('location/city/city/', views.city, name='city'),
    path('location/city/list_city/', views.listCity, name='list_city'),
    #path('ajax/load-cities/', views.load_provinces, name='ajax_load_cities'),
    path('location/city/city/ajax/ajax_provinces/<int:country_id>',views.ajax_provinces_city,name="ajax_provinces"),
    #path('ajax/ajax_provinces2/<int:id>',views.ajax_provinces,name="ajax_provinces2"),
    path('company/company_edit/<int:company_id>/ajax_provinces/<int:country_id>', views.ajax_provinces, name='ajax_provinces'),
    path('company/company_edit/<int:company_id>/ajax_citys/<int:province_id>', views.ajax_citys, name='ajax_cities'),
]

