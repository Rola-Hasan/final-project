from django.contrib import admin

from .models import Doctor, Specialization, InsuranceCompany, Governorate, UserProfile, Pharmacy, MedicalType, MedicalPhacility, Nurse, Schedule
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Specialization)
admin.site.register(InsuranceCompany)
admin.site.register(Governorate)
admin.site.register(UserProfile)
admin.site.register(Pharmacy)
admin.site.register(MedicalType)
admin.site.register(MedicalPhacility)
admin.site.register(Nurse)
admin.site.register(Schedule)
