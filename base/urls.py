from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('reset password/', views.forgot_passwordPage, name="forgot-password"),
    path('error/', views.errorPage, name="error"),
    path('add-doctor/', views.add_doctor, name="add_doctor"),
    path('add-pharmacy/', views.add_pharmacy, name="add_pharmacy"),
    path('add-nurse/', views.add_nurse, name="add_nurse"),
    path('add-medical-phacility/', views.add_medical_phacility,
         name="add_medical_phacility"),
    path('add-user/', views.add_user, name='add_user'),
    path('success/', views.success_page, name='success'),
    path('user-page/', views.userPage, name="userPage"),
    path('view-doctors/', views.viewDoctor, name="view_doctor"),
    path('view-nurses/', views.viewNurse, name="view_nurse"),
    path('view-pharmacies/', views.viewPharmacies, name="view_pharmacy"),
    path('view-medical-phacilities/', views.viewMedicalPhacilities,
         name="view_medical_phacilities"),
    path('Users/', views.viewUsers,
         name="view_users"),
    path('view-doctors-user/', views.viewDoctoruser, name="view_doctor_user"),
    path('Pharmacies/', views.viewPharmacyuser, name="view_pharmacy_user"),
    path('Medical-phacilities/', views.viewMedicalPhacilitiesuser,
         name="view_medical_phacility_user"),
    path('Nurses/', views.viewNurseuser,
         name="view_nurse_user"),
    path('doctor/<int:doctor_id>/schedule/',
         views.viewDoctorSchedule, name='doctor_schedule'),
    #     path('view-profile-settings/', views.profile_settings, name="profile_settings"),
    path('delete-doctor/<int:doctor_id>/',
         views.delete_doctor, name='delete_doctor'),
    path('delete-pharmacy/<int:pharmacy_id>/',
         views.delete_pharmacy, name='delete_pharmacy'),
    path('delete-phacility/<int:phacility_id>/',
         views.delete_phacility, name='delete_phacility'),
    path('delete-nurse/<int:nurse_id>/',
         views.delete_nurse, name='delete_nurse'),
    path('delete-schedule/<int:schedule_id>/',
         views.delete_schedule, name='delete_schedule'),
    path('get-select-options/', views.get_select_options,
         name='get_select_options'),  # Fetch select options
    path('update-doctor/<int:doctor_id>/',
         views.update_doctor, name='update_doctor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
