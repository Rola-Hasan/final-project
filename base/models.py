from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('regular_user', 'Regular User'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),

    ]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='regular_user')
    phone = models.CharField(max_length=20, null=True,
                             blank=True)  # Added field
    address = models.TextField(
        null=True, blank=True)               # Added field
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username

    def get_user_role(self):
        # Check if the user is in a specific group (role)
        if self.user.groups.filter(name="admin").exists():
            return "admin"
        elif self.user.groups.filter(name="regular_user").exists():
            return "regular_user"
        return "Unknown"


class Specialization(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MedicalType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Governorate(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE)
    insurancecompany = models.ForeignKey(
        InsuranceCompany, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    rate = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Schedule(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="schedules")
    day_of_week = models.CharField(
        max_length=9,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'start_time', 'end_time')
        ordering = ['day_of_week', 'start_time']

    def get_day_in_arabic(self):
        arabic_days = {
            'Monday': 'الاثنين',
            'Tuesday': 'الثلاثاء',
            'Wednesday': 'الأربعاء',
            'Thursday': 'الخميس',
            'Friday': 'الجمعة',
            'Saturday': 'السبت',
            'Sunday': 'الأحد',
        }
        return arabic_days.get(self.day_of_week, self.day_of_week)

    def __str__(self):
        return f"{self.doctor.firstname} {self.doctor.lastname} - {self.day_of_week}: {self.start_time} - {self.end_time}"


class Pharmacy(models.Model):
    name = models.CharField(max_length=200)
    insurancecompany = models.ForeignKey(
        InsuranceCompany, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    governorate = models.ForeignKey(
        Governorate, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    rate = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)

    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class MedicalPhacility(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(
        MedicalType, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE)
    insurancecompany = models.ForeignKey(
        InsuranceCompany, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    governorate = models.ForeignKey(
        Governorate, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    rate = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)

    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Nurse(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, null=True)
    insurancecompany = models.ForeignKey(
        InsuranceCompany, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    governorate = models.ForeignKey(
        Governorate, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    rate = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)

    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.firstname
