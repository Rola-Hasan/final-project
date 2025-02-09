# from .forms import UserProfileForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import UserProfile, Doctor, Specialization, InsuranceCompany, Governorate, Pharmacy, MedicalPhacility, MedicalType, Nurse, Schedule
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import time

from .forms import DoctorForm

# Create your views here.


@login_required(login_url='login')
@admin_only
def home(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    medical_phacilities = MedicalPhacility.objects.count()
    doctors = Doctor.objects.count()
    pharmacies = Pharmacy.objects.count()
    nurses = Nurse.objects.count()
    context = {'name': name, 'picture': picture, 'doctors': doctors, 'medical_phacilities': medical_phacilities, 'nurses': nurses,
               'pharmacies': pharmacies}
    return render(request, 'base/index.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password do not exist!')
    context = {}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    return render(request, 'base/register.html')


def forgot_passwordPage(request):
    return render(request, 'base/forgot-password.html')


def errorPage(request):
    return render(request, 'base/404.html')


def addDoctor(request):
    if request.method == 'POST':
        print(request.POST)
    context = {}
    return render(request, 'base/add-doctor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='regular_user')
def userPage(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    medical_phacilities = MedicalPhacility.objects.count()
    doctors = Doctor.objects.count()
    pharmacies = Pharmacy.objects.count()
    nurses = Nurse.objects.count()
    context = {'name': name, 'picture': picture, 'doctors': doctors, 'medical_phacilities': medical_phacilities, 'nurses': nurses,
               'pharmacies': pharmacies}
    return render(request, 'base/user-page.html', context)


@login_required(login_url='login')
@admin_only
def viewDoctor(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    doctors = Doctor.objects.all()
    insurancecompanies = InsuranceCompany.objects.all()
    specializations = Specialization.objects.all()
    governorates = Governorate.objects.all()

    context = {'doctors': doctors, 'insurancecompanies': insurancecompanies,
               'specializations': specializations, 'governorates': governorates, 'name': name, 'picture': picture}
    return render(request, 'base/view-doctors.html', context)


@login_required(login_url='login')
@admin_only
def viewPharmacies(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    pharmacies = Pharmacy.objects.all()
    context = {'pharmacies': pharmacies, 'name': name, 'picture': picture}
    return render(request, 'base/view-pharmacies.html', context)


@login_required(login_url='login')
@admin_only
def viewNurse(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    nurses = Nurse.objects.all()
    context = {'nurses': nurses, 'name': name, 'picture': picture}
    return render(request, 'base/view-nurse.html', context)


@login_required(login_url='login')
@admin_only
def viewMedicalPhacilities(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    medical_phaciliteis = MedicalPhacility.objects.all()
    context = {'medical_phaciliteis': medical_phaciliteis,
               'name': name, 'picture': picture}
    return render(request, 'base/view-medical-phacilities.html', context)


@login_required(login_url='login')
@admin_only
def viewUsers(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    userprofiles = UserProfile.objects.all()

    context = {'userprofiles': userprofiles,
               'name': name, 'picture': picture}
    return render(request, 'base/view-users.html', context)


@login_required(login_url='login')
@admin_only
def viewDoctorSchedule(request, doctor_id):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    doctor = get_object_or_404(Doctor, id=doctor_id)
    schedules = Schedule.objects.filter(
        doctor=doctor).order_by('day_of_week', 'start_time')

    context = {'doctor': doctor, 'schedules': schedules,
               'name': name, 'picture': picture}
    return render(request, 'base/schedule.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='regular_user')
def viewDoctoruser(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    doctors = Doctor.objects.all()
    context = {'doctors': doctors, 'name': name, 'picture': picture}
    return render(request, 'base/view-doctors-user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='regular_user')
def viewPharmacyuser(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    pharmacies = Pharmacy.objects.all()
    context = {'pharmacies': pharmacies, 'name': name, 'picture': picture}
    return render(request, 'base/view-pharmacies-user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='regular_user')
def viewMedicalPhacilitiesuser(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    medical_phacilities = MedicalPhacility.objects.all()
    context = {'medical_phacilities': medical_phacilities,
               'name': name, 'picture': picture}
    return render(request, 'base/view-medical-phacility-user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='regular_user')
def viewNurseuser(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    nurses = Nurse.objects.all()
    context = {'nurses': nurses,
               'name': name, 'picture': picture}
    return render(request, 'base/view-nurse-user.html', context)


def success_page(request):
    return render(request, 'base/success.html')


def add_doctor(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        specialization_id = request.POST.get('specialization')
        address = request.POST.get('address')
        governorate_id = request.POST.get('governorate')
        insurance_company_id = request.POST.get('insurance_company')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        days = request.POST.getlist('days[]')
        start_times = request.POST.getlist('start_times[]')
        end_times = request.POST.getlist('end_times[]')

        # Validation (can be extended as needed)
        if not (firstname and lastname and gender and specialization_id and address and phone):
            messages.error(request, "All fields are required.")
            return redirect('add_doctor')

        try:
            # Retrieve related objects
            specialization = get_object_or_404(
                Specialization, pk=specialization_id)
            governorate = get_object_or_404(Governorate, pk=governorate_id)
            insurance_company = get_object_or_404(
                InsuranceCompany, pk=insurance_company_id)

            # Save Doctor
            doctor = Doctor.objects.create(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                specialization=specialization,
                address=address,
                governorate=governorate,
                insurancecompany=insurance_company,
                phone_number=phone,
                description=description
            )

            # Save Schedule
            for day, start, end in zip(days, start_times, end_times):
                Schedule.objects.create(
                    doctor=doctor, day_of_week=day, start_time=start, end_time=end)

            messages.success(request, "Doctor added successfully!")
            return redirect('view_doctor')  # Update to your list view name
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_doctor')

    # Load additional data for the form
    context = {
        'specializations': Specialization.objects.all(),
        'governorates': Governorate.objects.all(),
        'insurance_companies': InsuranceCompany.objects.all(),
        'picture': request.user.userprofile.profile_picture,
        'name': request.user.username
    }
    return render(request, 'base/add-doctor.html', context)


@csrf_exempt
def get_doctor_schedules(request, doctor_id):
    if request.method == "GET":
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            schedules = Schedule.objects.filter(doctor=doctor)
            schedules_data = [
                {
                    "day_of_week": schedule.day_of_week,
                    "start_time": str(schedule.start_time),
                    "end_time": str(schedule.end_time)
                }
                for schedule in schedules
            ]
            return JsonResponse({"doctor": str(doctor), "schedules": schedules_data}, status=200)
        except Doctor.DoesNotExist:
            return JsonResponse({"error": "Doctor not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def add_pharmacy(request):
    name = request.user.username
    if request.method == 'POST':
        name = request.POST.get('pharmacy_name')  # First Name
        insurancecompany_id = request.POST.get(
            'insurance')     # Insurance Company
        phone_number = request.POST.get('phone')      # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')         # Address
        # Address

        # Foreign keys lookup

        insurancecompany = InsuranceCompany.objects.get(id=insurancecompany_id)
        governorate = Governorate.objects.get(id=governorate_id)

        # Create the Doctor instance

        pharmacy = Pharmacy(
            name=name,
            insurancecompany=insurancecompany,
            phone_number=phone_number,
            governorate=governorate,
            address=address)

        pharmacy.save()
        # Redirect to a success page after saving
        return redirect('add_pharmacy')

    # Pass the required data for the dropdowns

    insurance_companies = InsuranceCompany.objects.all()
    governorates = Governorate.objects.all()

    return render(request, 'base/add-pharmacy.html', {

        'insurance_companies': insurance_companies,
        'governorates': governorates,
        'name': name,
        'picture': request.user.userprofile.profile_picture,
    })


def add_medical_phacility(request):
    name = request.user.username
    if request.method == 'POST':
        name = request.POST.get('medical_phacility_name')  # First Name

        # Gender
        specialization_id = request.POST.get(
            'specialization')  # Specialization
        medical_type_id = request.POST.get(
            'type')  # Specialization
        insurancecompany_id = request.POST.get(
            'insurance')     # Insurance Company
        phone_number = request.POST.get('phone')      # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')         # Address

        # Foreign keys lookup
        medical_type = MedicalType.objects.get(id=medical_type_id)
        specialization = Specialization.objects.get(id=specialization_id)
        insurancecompany = InsuranceCompany.objects.get(id=insurancecompany_id)
        governorate = Governorate.objects.get(id=governorate_id)

        # Create the Doctor instance
        medical_phacility = MedicalPhacility(
            name=name,
            type=medical_type,
            specialization=specialization,
            insurancecompany=insurancecompany,
            phone_number=phone_number,
            governorate=governorate,
            address=address
        )
        medical_phacility.save()
        # Redirect to a success page after saving
        return redirect('add_medical_phacility')

    # Pass the required data for the dropdowns
    medicaltypes = MedicalType.objects.all()
    specializations = Specialization.objects.all()
    insurance_companies = InsuranceCompany.objects.all()
    governorates = Governorate.objects.all()

    return render(request, 'base/add-medical-phacility.html', {
        'medicaltypes': medicaltypes,
        'specializations': specializations,
        'insurance_companies': insurance_companies,
        'governorates': governorates,
        'name': name,
        'picture': request.user.userprofile.profile_picture,

    })


def add_nurse(request):
    name = request.user.username
    if request.method == 'POST':
        firstname = request.POST.get('fname')  # First Name
        lastname = request.POST.get('lname')   # Last Name
        gender = request.POST.get('gender')           # Gender
        insurancecompany_id = request.POST.get(
            'insurance')     # Insurance Company
        phone_number = request.POST.get('phone')      # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')         # Address

        # Foreign keys lookup

        insurancecompany = InsuranceCompany.objects.get(id=insurancecompany_id)
        governorate = Governorate.objects.get(id=governorate_id)

        # Create the Doctor instance
        nurse = Nurse(
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            insurancecompany=insurancecompany,
            phone_number=phone_number,
            governorate=governorate,
            address=address
        )
        nurse.save()
        # Redirect to a success page after saving
        return redirect('add_nurse')

    # Pass the required data for the dropdowns

    insurance_companies = InsuranceCompany.objects.all()
    governorates = Governorate.objects.all()

    return render(request, 'base/add-nurse.html', {

        'insurance_companies': insurance_companies,
        'governorates': governorates,
        'name': name,
        'picture': request.user.userprofile.profile_picture,

    })


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        role = request.POST.get('role')  # 'admin' or 'regular_user'
        profile_picture = request.FILES.get('profile_picture')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        description = request.POST.get('description')

        try:
            # Create User object
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Add user to the selected group (admin or regular_user)
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            # Create UserProfile object
            user_profile = UserProfile.objects.create(
                user=user,
                gender=gender,
                role=role,
                profile_picture=profile_picture,
            )
            user_profile.phone = phone
            user_profile.address = address
            user_profile.description = description
            user_profile.save()

            messages.success(
                request, 'User created and added to group successfully!')
            return redirect('view_users')

        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')

    return render(request, 'base/add-user.html')


def delete_doctor(request, doctor_id):
    # Ensure the request is a DELETE request
    if request.method == 'DELETE':
        doctor = get_object_or_404(Doctor, id=doctor_id)

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.delete()
            return JsonResponse({'success': True})
        except Doctor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doctor not found.'})


def delete_pharmacy(request, pharmacy_id):
    # Ensure the request is a DELETE request
    if request.method == 'DELETE':
        pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)

        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
            pharmacy.delete()
            return JsonResponse({'success': True})
        except Pharmacy.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pharmacy not found.'})

    # If the request method is not DELETE, return an error


def delete_phacility(request, phacility_id):
    # Ensure the request is a DELETE request
    if request.method == 'DELETE':
        phacility = get_object_or_404(MedicalPhacility, id=phacility_id)

        try:
            phacility = MedicalPhacility.objects.get(id=phacility_id)
            phacility.delete()
            return JsonResponse({'success': True})
        except MedicalPhacility.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'phacility not found.'})

    # If the request method is not DELETE, return an error


def delete_nurse(request, nurse_id):
    # Ensure the request is a DELETE request
    if request.method == 'DELETE':
        nurse = get_object_or_404(Nurse, id=nurse_id)

        try:
            nurse = Nurse.objects.get(id=nurse_id)
            nurse.delete()
            return JsonResponse({'success': True})
        except Nurse.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'nurse not found.'})

    # If the request method is not DELETE, return an error


@csrf_exempt
def delete_schedule(request, schedule_id):
    if request.method == 'DELETE':
        try:
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.delete()
            return JsonResponse({'success': True})
        except Schedule.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Schedule not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_select_options(request):
    if request.method == 'GET':
        specializations = list(Specialization.objects.values('id', 'name'))
        insurance_companies = list(
            InsuranceCompany.objects.values('id', 'name'))
        governorates = list(Governorate.objects.values('id', 'name'))
        genders = [{'id': 'male', 'name': 'Male'},
                   {'id': 'female', 'name': 'Female'}]

        return JsonResponse({
            'specializations': specializations,
            'insurance_companies': insurance_companies,
            'governorates': governorates,
            'genders': genders,
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def update_doctor(request, doctor_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.firstname = data['firstname']
            doctor.lastname = data['lastname']
            doctor.gender = data['gender']
            doctor.specialization = data['specialization']
            doctor.insurancecompany = data['insurancecompany']
            doctor.governorate = data['governorate']
            doctor.save()
            return JsonResponse({"success": True})
        except Doctor.DoesNotExist:
            return JsonResponse({"success": False, "error": "Doctor not found"}, status=404)


# views.py


# views.py


# @login_required
# def profile_settings(request):
#     # This will work after the signal creates the profile
#     user_profile = request.user.profile

#     if request.method == 'POST':
#         form = UserProfileForm(
#             request.POST, request.FILES, instance=user_profile)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('profile_settings')

#     else:
#         form = UserProfileForm(instance=user_profile)

#     return render(request, 'base/profile.html', {'form': form})
