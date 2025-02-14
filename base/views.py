# from .forms import UserProfileForm
import math
import requests
from .models import Doctor, Specialization, Governorate, InsuranceCompany, Schedule
from .models import InsuranceCompany, Governorate
from .models import Nurse, Governorate, InsuranceCompany
from .models import UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404, redirect
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
def viewInsurance(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    insurance_companies = InsuranceCompany.objects.all()
    context = {'insurance_companies': insurance_companies,
               'name': name, 'picture': picture}
    return render(request, 'base/view-insurance.html', context)


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
def viewDoctorSchedule(request, doctor_id):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    doctor = get_object_or_404(Doctor, id=doctor_id)
    schedules = Schedule.objects.filter(
        doctor=doctor).order_by('day_of_week', 'start_time')
    address = doctor.address
    doc_picture = doctor.profile_picture
    phone_number = doctor.phone_number
    description = doctor.description
    context = {'doctor': doctor, 'schedules': schedules,
               'name': name, 'picture': picture, 'address': address, 'doc_picture': doc_picture,
               'phone_number': phone_number, 'description': description}
    return render(request, 'base/schedule.html', context)


@login_required(login_url='login')
def viewPharmacyDetails(request, pharmacy_id):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)

    address = pharmacy.address
    pha_picture = pharmacy.profile_picture
    phone_number = pharmacy.phone_number
    description = pharmacy.description
    context = {'pharmacy': pharmacy,
               'name': name, 'picture': picture, 'address': address, 'pha_picture': pha_picture,
               'phone_number': phone_number, 'description': description}
    return render(request, 'base/view-pharmacy-details.html', context)


@login_required(login_url='login')
def viewInsuranceCompanyDetails(request, insurance_company_id):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    insurance_company = get_object_or_404(
        InsuranceCompany, id=insurance_company_id)

    address = insurance_company.address

    description = insurance_company.description
    context = {'insurance_company': insurance_company,
               'name': name, 'picture': picture, 'address': address,  'description': description}
    return render(request, 'base/view-insurance-details.html', context)


@login_required(login_url='login')
def viewNurseDetails(request, nurse_id):
    user_name = request.user.username
    picture = request.user.userprofile.profile_picture
    nurse = get_object_or_404(Nurse, id=nurse_id)

    address = nurse.address
    nurse_picture = nurse.profile_picture
    phone_number = nurse.phone_number
    description = nurse.description
    context = {'nurse': nurse,
               'user_name': user_name, 'picture': picture, 'address': address, 'nurse_picture': nurse_picture,
               'phone_number': phone_number, 'description': description}
    return render(request, 'base/view-nurse-details.html', context)


@login_required(login_url='login')
def viewMedicalDetails(request, medical_phacility_id):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    medical_phacility = get_object_or_404(
        MedicalPhacility, id=medical_phacility_id)

    address = medical_phacility.address
    med_picture = medical_phacility.profile_picture
    phone_number = medical_phacility.phone_number
    description = medical_phacility.description
    context = {'medical_phacility': medical_phacility,
               'name': name, 'picture': picture, 'address': address, 'med_picture': med_picture,
               'phone_number': phone_number, 'description': description}
    return render(request, 'base/view-medical-phacility-details.html', context)


@login_required(login_url='login')
@admin_only
def viewUserDetails(request, userprofile_id):
    userprofile = get_object_or_404(UserProfile, id=userprofile_id)

# Get the associated user
    user1 = userprofile.user

# Get first and last name
    first_name = user1.first_name if user1 else "Unknown"
    last_name = user1.last_name if user1 else "Unknown"

    # Get other user profile details
    address = userprofile.address
    userprofile_picture = userprofile.profile_picture
    phone_number = userprofile.phone
    description = userprofile.description
    gender = userprofile.gender

    name = request.user.username
    picture = request.user.userprofile.profile_picture

    context = {'userprofile': userprofile,
               'name': name, 'picture': picture, 'first_name': first_name, 'last_name': last_name, 'address': address, 'userprofile_picture': userprofile_picture,
               'phone_number': phone_number, 'gender': gender, 'description': description}
    return render(request, 'base/view-user-details.html', context)


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


@login_required(login_url='login')
@allowed_users(allowed_roles='regular_user')
def viewInsuranceuser(request):
    name = request.user.username
    picture = request.user.userprofile.profile_picture
    insurance_companies = InsuranceCompany.objects.all()
    context = {'insurance_companies': insurance_companies,
               'name': name, 'picture': picture}
    return render(request, 'base/view-insurance-user.html', context)


def success_page(request):
    return render(request, 'base/success.html')


# Haversine formula to calculate distance between two points on the Earth

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


# Define your OpenCage API key
API_KEY = 'b8a28645e2534deb9357e1da1563ba75'  # Replace with your actual API key

# Function to get latitude and longitude from OpenCage API


def get_coordinates(address):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={address}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Check if the API response contains results
    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lon = data['results'][0]['geometry']['lng']
        return lat, lon
    else:
        return None, None


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
        picture = request.FILES.get('picture')
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

            # Get latitude and longitude from the address using OpenCage API
            latitude, longitude = get_coordinates(address)
            if not latitude or not longitude:
                messages.error(
                    request, "Could not get coordinates for the provided address.")
                return redirect('add_doctor')

            # Save Doctor with coordinates (latitude and longitude)
            doctor = Doctor.objects.create(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                specialization=specialization,
                address=address,
                governorate=governorate,
                insurancecompany=insurance_company,
                phone_number=phone,
                profile_picture=picture,
                description=description,
                latitude=latitude,  # Store latitude
                longitude=longitude,  # Store longitude
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
def get_doctor_details(request, doctor_id):
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


def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    schedules = Schedule.objects.filter(doctor=doctor)

    if request.method == 'POST':
        try:
            # Update doctor details
            doctor.firstname = request.POST.get('firstname')
            doctor.lastname = request.POST.get('lastname')
            doctor.gender = request.POST.get('gender')
            doctor.specialization = get_object_or_404(
                Specialization, pk=request.POST.get('specialization'))
            doctor.address = request.POST.get('address')
            doctor.governorate = get_object_or_404(
                Governorate, pk=request.POST.get('governorate'))
            doctor.insurancecompany = get_object_or_404(
                InsuranceCompany, pk=request.POST.get('insurance_company'))
            doctor.phone_number = request.POST.get('phone')

            # Only update profile picture if a new one is uploaded
            new_picture = request.FILES.get('picture')
            if new_picture:
                doctor.profile_picture = new_picture

            doctor.description = request.POST.get('description')
            doctor.save()

            # Handle schedules update
            days = request.POST.getlist('days[]')
            start_times = request.POST.getlist('start_times[]')
            end_times = request.POST.getlist('end_times[]')

            # Update existing schedules if possible, otherwise create new ones
            existing_schedules = list(schedules)

            for index, (day, start, end) in enumerate(zip(days, start_times, end_times)):
                if index < len(existing_schedules):  # Update existing schedule
                    schedule = existing_schedules[index]
                    schedule.day_of_week = day
                    schedule.start_time = start
                    schedule.end_time = end
                    schedule.save()
                else:  # Create new schedule if there are more inputs than existing schedules
                    Schedule.objects.create(
                        doctor=doctor, day_of_week=day, start_time=start, end_time=end
                    )

            # If there are extra old schedules, delete them
            if len(existing_schedules) > len(days):
                for extra_schedule in existing_schedules[len(days):]:
                    extra_schedule.delete()

            messages.success(request, "Doctor updated successfully!")
            return redirect('view_doctor')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    context = {
        'doctor': doctor,
        'specializations': Specialization.objects.all(),
        'governorates': Governorate.objects.all(),
        'insurance_companies': InsuranceCompany.objects.all(),
        'schedules': schedules,
    }
    return render(request, 'base/edit-doctor.html', context)


def add_pharmacy(request):
    name = request.user.username
    if request.method == 'POST':
        name = request.POST.get('pharmacy_name')  # Pharmacy Name
        insurancecompany_id = request.POST.get(
            'insurance')  # Insurance Company
        phone_number = request.POST.get('phone')  # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')
        pha_picture = request.FILES.get('picture')  # Profile Picture

        # Foreign keys lookup
        # Handle the case where 'insurancecompany_id' is empty (i.e., "لا يوجد" option is selected)
        if insurancecompany_id:
            insurancecompany = InsuranceCompany.objects.get(
                id=insurancecompany_id)
        else:
            insurancecompany = None  # Set the insurance company to None if "لا يوجد" is selected

        # Handle the governorate lookup
        governorate = Governorate.objects.get(id=governorate_id)

        # Get coordinates for the address
        latitude, longitude = get_coordinates(address)
        if not latitude or not longitude:
            messages.error(
                request, "Could not get coordinates for the provided address.")
            return redirect('add_pharmacy')

        # Create the new pharmacy instance
        pharmacy = Pharmacy(
            name=name,
            insurancecompany=insurancecompany,  # This can be None
            phone_number=phone_number,
            governorate=governorate,
            address=address,
            profile_picture=pha_picture,
            latitude=latitude,
            longitude=longitude,
        )

        pharmacy.save()  # Save the pharmacy instance to the database

        # Redirect to the success page
        return redirect('view_pharmacy')

    # Fetch the dropdown options
    insurance_companies = InsuranceCompany.objects.all()
    governorates = Governorate.objects.all()

    return render(request, 'base/add-pharmacy.html', {
        'insurance_companies': insurance_companies,
        'governorates': governorates,
        'name': name,
        'picture': request.user.userprofile.profile_picture,
    })


def edit_pharmacy(request, pharmacy_id):
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    user_name = request.user.username

    if request.method == 'POST':
        name = request.POST.get('pharmacy_name')  # Pharmacy Name
        insurancecompany_id = request.POST.get(
            'insurance')  # Insurance Company
        phone_number = request.POST.get('phone')  # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')  # Address
        pha_picture = request.FILES.get('picture')  # Profile Picture

        # Foreign key lookups
        # Check if 'insurancecompany_id' is empty (i.e., "لا يوجد" was selected)
        if insurancecompany_id:
            insurancecompany = InsuranceCompany.objects.get(
                id=insurancecompany_id)
        else:
            insurancecompany = None  # Set to None if "لا يوجد" is selected

        governorate = Governorate.objects.get(id=governorate_id)

        # Update the pharmacy instance
        pharmacy.name = name
        pharmacy.insurancecompany = insurancecompany
        pharmacy.phone_number = phone_number
        pharmacy.governorate = governorate
        pharmacy.address = address

        # Update the profile picture only if a new one is uploaded
        if pha_picture:
            pharmacy.profile_picture = pha_picture

        pharmacy.save()  # Save the updated pharmacy

        return redirect('view_pharmacy')

    # Fetch dropdown options for insurance companies and governorates
    insurance_companies = InsuranceCompany.objects.all()
    governorates = Governorate.objects.all()

    return render(request, 'base/edit-pharmacy.html', {
        'pharmacy': pharmacy,
        'insurance_companies': insurance_companies,
        'governorates': governorates,
        'user_name': user_name,
        'picture': request.user.userprofile.profile_picture,
    })


def add_medical_phacility(request):
    name = request.user.username
    if request.method == 'POST':
        med_name = request.POST.get('medical_phacility_name')  # First Name

        # Gender
        specialization_id = request.POST.get(
            'specialization')  # Specialization
        medical_type_id = request.POST.get(
            'type')  # Specialization
        insurancecompany_id = request.POST.get(
            'insurance')     # Insurance Company
        phone_number = request.POST.get('phone')      # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')
        med_picture = request.FILES.get('picture')  # Address

        # Foreign keys lookup
        medical_type = MedicalType.objects.get(id=medical_type_id)
        specialization = Specialization.objects.get(id=specialization_id)
        insurancecompany = InsuranceCompany.objects.get(id=insurancecompany_id)
        governorate = Governorate.objects.get(id=governorate_id)
        latitude, longitude = get_coordinates(address)
        if not latitude or not longitude:
            messages.error(
                request, "Could not get coordinates for the provided address.")
            return redirect('add_medical_phacility')

        # Create the Doctor instance
        medical_phacility = MedicalPhacility(
            name=med_name,
            type=medical_type,
            specialization=specialization,
            insurancecompany=insurancecompany,
            phone_number=phone_number,
            governorate=governorate,
            address=address,
            profile_picture=med_picture,
            latitude=latitude,  # Store latitude
            longitude=longitude,
        )
        medical_phacility.save()
        # Redirect to a success page after saving
        return redirect('view_medical_phacilities')

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


def edit_medical_phacility(request, medical_phacility_id):
    medical_phacility = get_object_or_404(
        MedicalPhacility, id=medical_phacility_id)
    user_name = request.user.username

    if request.method == 'POST':
        med_name = request.POST.get('medical_phacility_name')  # Name
        specialization_id = request.POST.get(
            'specialization')  # Specialization
        medical_type_id = request.POST.get('type')  # Medical Type
        insurancecompany_id = request.POST.get(
            'insurance_company')  # Insurance Company
        phone_number = request.POST.get('phone')  # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')
        med_picture = request.FILES.get('picture')  # Profile Picture

        # Foreign keys lookup
        medical_type = MedicalType.objects.get(id=medical_type_id)
        specialization = Specialization.objects.get(id=specialization_id)
        insurancecompany = InsuranceCompany.objects.get(id=insurancecompany_id)
        governorate = Governorate.objects.get(id=governorate_id)

        # **Updating** the existing medical_phacility instance instead of creating a new one
        medical_phacility.name = med_name
        medical_phacility.type = medical_type
        medical_phacility.specialization = specialization
        medical_phacility.insurancecompany = insurancecompany
        medical_phacility.phone_number = phone_number
        medical_phacility.governorate = governorate
        medical_phacility.address = address

        if med_picture:
            medical_phacility.profile_picture = med_picture

        medical_phacility.save()  # Save the updated instance

        return redirect('view_medical_phacilities')

    # Pass the required data for the dropdowns
    medicaltypes = MedicalType.objects.all()
    specializations = Specialization.objects.all()
    insurance_companies = InsuranceCompany.objects.all()
    governorates = Governorate.objects.all()

    return render(request, 'base/edit-medical-phacility.html', {
        'medical_phacility': medical_phacility,
        'medicaltypes': medicaltypes,
        'specializations': specializations,
        'insurance_companies': insurance_companies,
        'governorates': governorates,
        'user_name': user_name,
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
        address = request.POST.get('address')
        nurse_picture = request.FILES.get('picture')
        description = request.POST.get('description')  # Address

        # Foreign keys lookup

        insurancecompany = InsuranceCompany.objects.get(id=insurancecompany_id)
        governorate = Governorate.objects.get(id=governorate_id)
        # Get latitude and longitude from the address using OpenCage API
        latitude, longitude = get_coordinates(address)
        if not latitude or not longitude:
            messages.error(
                request, "Could not get coordinates for the provided address.")
            return redirect('add_nurse')

        # Create the Doctor instance
        nurse = Nurse(
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            insurancecompany=insurancecompany,
            phone_number=phone_number,
            governorate=governorate,
            address=address,
            profile_picture=nurse_picture,
            description=description,
            latitude=latitude,  # Store latitude
            longitude=longitude,
        )
        nurse.save()
        # Redirect to a success page after saving
        return redirect('view_nurse')

    # Pass the required data for the dropdowns

    insurance_companies = InsuranceCompany.objects.all()
    governorates = Governorate.objects.all()

    return render(request, 'base/add-nurse.html', {

        'insurance_companies': insurance_companies,
        'governorates': governorates,
        'name': name,
        'picture': request.user.userprofile.profile_picture,

    })


def edit_nurse(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)

    if request.method == 'POST':
        try:
            # Update nurse details
            nurse.firstname = request.POST.get('fname')
            nurse.lastname = request.POST.get('lname')
            nurse.gender = request.POST.get('gender')
            nurse.governorate = get_object_or_404(
                Governorate, pk=request.POST.get('governorate'))
            nurse.insurancecompany = get_object_or_404(
                InsuranceCompany, pk=request.POST.get('insurance'))
            nurse.phone_number = request.POST.get('phone')
            nurse.address = request.POST.get('address')
            nurse.description = request.POST.get('description')

            # Only update profile picture if a new one is uploaded
            new_picture = request.FILES.get('picture')
            if new_picture:
                nurse.profile_picture = new_picture

            nurse.save()
            messages.success(request, "Nurse updated successfully!")
            return redirect('view_nurse')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    context = {
        'nurse': nurse,
        'governorates': Governorate.objects.all(),
        'insurance_companies': InsuranceCompany.objects.all(),
    }
    return render(request, 'base/edit-nurse.html', context)


@login_required
def add_user(request):
    name = request.user.username

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        role = request.POST.get('role')  # 'admin' or 'regular_user'
        profile_picture = request.FILES.get('profile_picture')  # File upload
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        description = request.POST.get('description')

        try:
            # Debugging print statements
            print("POST Data:", request.POST)
            print("FILES Data:", request.FILES)

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('add_user')

            # Create User object with hashed password
            user = User.objects.create(
                username=username,
                password=make_password(password),  # Hashing password
                first_name=first_name,
                last_name=last_name
            )

            # Add user to the selected group (admin or regular_user)
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            # Fetch or create UserProfile instead of blindly creating it
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "gender": gender,
                    "role": role,
                    "profile_picture": profile_picture if profile_picture else None,
                    "phone": phone,
                    "address": address if address else "",
                    "description": description if description else "",
                }
            )

            if not created:
                # If profile already exists, update the fields
                user_profile.gender = gender
                user_profile.role = role
                user_profile.phone = phone
                user_profile.address = address if address else ""
                user_profile.description = description if description else ""
                if profile_picture:
                    user_profile.profile_picture = profile_picture
                user_profile.save()

            messages.success(request, "User created and added successfully!")
            return redirect('view_users')  # Adjust the redirect URL as needed

        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")

    return render(request, 'base/add-user.html', {
        'name': name,
        'picture': getattr(request.user.userprofile, 'profile_picture', None),
    })


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        try:
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password')
                              ) if request.POST.get('password') else None
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            user_profile.gender = request.POST.get('gender')
            user_profile.role = request.POST.get('role')
            user_profile.phone = request.POST.get('phone')
            user_profile.address = request.POST.get('address')
            user_profile.description = request.POST.get('description')

            new_picture = request.FILES.get('profile_picture')
            if new_picture:
                user_profile.profile_picture = new_picture

            user_profile.save()

            # Update user role in groups
            admin_group, _ = Group.objects.get_or_create(name='admin')
            regular_user_group, _ = Group.objects.get_or_create(
                name='regular_user')

            user.groups.clear()
            if user_profile.role == 'admin':
                user.groups.add(admin_group)
            else:
                user.groups.add(regular_user_group)

            messages.success(request, "User updated successfully!")
            return redirect('view_users')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'base/edit-user.html', context)


def add_insurance_company(request):
    name = request.user.username
    if request.method == 'POST':
        name = request.POST.get('fname')  # First Name
        phone_number = request.POST.get('phone')      # Phone Number
        governorate_id = request.POST.get('governorate')  # Governorate
        address = request.POST.get('address')         # Address
        discription = request.POST.get('description')
        # Foreign keys lookup

        governorate = Governorate.objects.get(id=governorate_id)

        # Create the Doctor instance
        insurance = InsuranceCompany(
            name=name,
            phone_number=phone_number,
            governorate=governorate,
            address=address,
            description=discription
        )
        insurance.save()
        # Redirect to a success page after saving
        return redirect('add_insurance')

    # Pass the required data for the dropdowns

    governorates = Governorate.objects.all()

    return render(request, 'base/add-insurance.html', {


        'governorates': governorates,
        'name': name,
        'picture': request.user.userprofile.profile_picture,

    })


def edit_insurance_company(request, insurance_company_id):
    insurance_company = get_object_or_404(
        InsuranceCompany, id=insurance_company_id)

    if request.method == 'POST':
        try:
            # Update insurance company details
            insurance_company.name = request.POST.get('fname')
            insurance_company.governorate = get_object_or_404(
                Governorate, pk=request.POST.get('governorate'))
            insurance_company.address = request.POST.get('address')
            insurance_company.phone_number = request.POST.get('phone')
            insurance_company.description = request.POST.get('description')

            insurance_company.save()

            messages.success(request, "تم تعديل شركة التأمين بنجاح!")
            return redirect('view_insurance')

        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")

    context = {
        'insurance_company': insurance_company,
        'governorates': Governorate.objects.all(),
    }
    return render(request, 'base/edit-insurance-company.html', context)


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


# Allows AJAX request to bypass CSRF (only for testing; remove in production)


@csrf_exempt
def delete_userprofile(request, userprofile_id):
    if request.method == 'POST':
        userprofile = get_object_or_404(UserProfile, id=userprofile_id)

        try:
            # Store the associated user before deleting the profile
            user = userprofile.user

            # Delete the UserProfile
            userprofile.delete()

            # Delete the associated User (if exists)
            if user:
                user.delete()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def delete_insurance_company(request, insurance_company_id):
    # Ensure the request is a DELETE request
    if request.method == 'DELETE':
        insurance_company = get_object_or_404(
            InsuranceCompany, id=insurance_company_id)

        try:
            insurance_company.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


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
