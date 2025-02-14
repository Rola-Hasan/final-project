from django.urls import path
from . import views

urlpatterns = [

    path('', views.main_home, name='main_home1'),
    path('about/', views.about, name='about'),

    path('doctors/<int:governorate_id>/<int:specialization_id>/',
         views.doctors_in_governorate, name='doctors_in_governorate'),
    path('facilities/<int:governorate_id>/<int:facility_type_id>/',
         views.facilities_in_governorate, name='facilities_in_governorate'),
    path('nurses/<int:governorate_id>/',
         views.nurses_in_governorate, name='nurses_in_governorate'),
    path('pharmacies/<int:governorate_id>/',
         views.pharmacies_in_governorate, name='pharmacies_in_governorate'),
    path('search/', views.search, name='search'),


    path('search_by_location/', views.search_by_location,
         name='search_by_location'),
    path('search_nurse_by_location/', views.search_nearest_nurse,
         name='search_nearest_nurse1'),
    path('search_facility_by_location/', views.search_nearest_medical_facility,
         name='search_nearest_medical_facility1'),
    path('search_pharmacy_by_location/', views.search_nearest_pharmacy,
         name='search_nearest_pharmacy1'),

    path('save_location/', views.set_location,
         name='save_location'),


]
