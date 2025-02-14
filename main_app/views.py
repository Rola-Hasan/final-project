

from base.models import Doctor
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.shortcuts import render, redirect
import math

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

from base.models import Doctor, Governorate, Specialization, Pharmacy, MedicalPhacility, Nurse, MedicalType
from django.shortcuts import render, get_object_or_404, redirect
from geopy.geocoders import Nominatim


# Create your views here.

from django.shortcuts import render


def main_home(request):
    # Clear the specific location data from the session

    return render(request, 'main_app/index.html')


def about(request):
    return render(request, 'main_app/about_us.html')


def doctors_in_governorate(request, governorate_id, specialization_id):
    governorate = get_object_or_404(Governorate, id=governorate_id)
    specialization = get_object_or_404(Specialization, id=specialization_id)
    doctors = Doctor.objects.filter(
        governorate=governorate, specialization=specialization)

    return render(request, 'main_app/doctor.html', {
        'doctors': doctors,
        'governorate': governorate,
        'specialization': specialization
    })


def facilities_in_governorate(request, governorate_id, facility_type_id):
    governorate = get_object_or_404(Governorate, id=governorate_id)
    facility_type = get_object_or_404(MedicalType, id=facility_type_id)
    facilities = MedicalPhacility.objects.filter(
        governorate=governorate, facility_type=facility_type)

    return render(request, 'main_app/facility_list.html', {
        'facilities': facilities,
        'governorate': governorate,
        'facility_type': facility_type
    })


def nurses_in_governorate(request, governorate_id):
    governorate = get_object_or_404(Governorate, id=governorate_id)
    nurses = Nurse.objects.filter(governorate=governorate)

    return render(request, 'main_app/nurse_list.html', {
        'nurses': nurses,
        'governorate': governorate,
    })


def pharmacies_in_governorate(request, governorate_id):
    governorate = get_object_or_404(Governorate, id=governorate_id)
    pharmacies = Pharmacy.objects.filter(governorate=governorate)

    return render(request, 'main_app/pharmacy_list.html', {
        'pharmacies': pharmacies,
        'governorate': governorate,
    })


def search(request):
    query = request.GET.get('q', '')  # Get the search query from the request

    doctors = Doctor.objects.filter(
        Q(firstname__icontains=query) | Q(lastname__icontains=query)
    )
    pharmacies = Pharmacy.objects.filter(name__icontains=query)
    medical_facilities = MedicalPhacility.objects.filter(name__icontains=query)
    nurses = Nurse.objects.filter(
        Q(firstname__icontains=query) | Q(lastname__icontains=query)
    )

    # Return the search results as context to the template
    context = {
        'doctors': doctors,
        'pharmacies': pharmacies,
        'medical_facilities': medical_facilities,
        'nurses': nurses,
        'query': query
    }
    return render(request, 'main_app/navigate.html', context)


def location_search(request):
    """
    Search based on user's current location.
    Redirects to index page if location is not available.
    """
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')

    if latitude and longitude:
        doctors = Doctor.objects.filter(
            location__latitude=latitude, location__longitude=longitude)
        nurses = Nurse.objects.filter(
            location__latitude=latitude, location__longitude=longitude)
        pharmacies = Pharmacy.objects.filter(
            location__latitude=latitude, location__longitude=longitude)
        medical_facilities = MedicalPhacility.objects.filter(
            location__latitude=latitude, location__longitude=longitude)

        return render(request, 'main_app/search-by-location.html', {
            'doctors': doctors,
            'nurses': nurses,
            'pharmacies': pharmacies,
            'medical_facilities': medical_facilities
        })
    else:
        messages.error(
            request, "Location access is required for this feature. Please enable location services.")
        return redirect('main_home')


@csrf_exempt
def set_location(request):
    """
    Saves user location from frontend and redirects to search-by-location.
    """
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        if latitude and longitude:
            request.session["latitude"] = latitude
            request.session["longitude"] = longitude
            request.session["location_shared"] = True
            return redirect('location_search')

    messages.error(request, "Failed to retrieve location. Please try again.")
    return redirect('main_home')


# Haversine formula to calculate distance between two points

def haversine(lat1, lon1, lat2, lon2):
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        # Return a large distance if any coordinate is missing
        return float('inf')

    R = 6371.0  # Radius of Earth in km
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def search_by_location(request):
    # Retrieve user location from session
    user_lat = request.session.get("latitude")
    user_lon = request.session.get("longitude")

    # If location is missing, redirect to home or request location
    if user_lat is None or user_lon is None:
        messages.error(
            request, "Your location is required to find nearby doctors.")
        # Redirect to the homepage where user can allow location
        return redirect("main_home1")

    # Retrieve all doctors
    doctors = Doctor.objects.all()
    nearest_doctors = []

    for doctor in doctors:
        # Ensure doctor has valid latitude & longitude
        if doctor.latitude is None or doctor.longitude is None:
            continue  # Skip this doctor if location is missing

        # Calculate distance using Haversine formula
        distance = haversine(float(user_lat), float(user_lon), float(
            doctor.latitude), float(doctor.longitude))

        nearest_doctors.append({
            "doctor": doctor,
            "distance": distance
        })

    # Sort doctors by distance (nearest first)
    nearest_doctors.sort(key=lambda x: x["distance"])

    return render(request, "main_app/search-by-location.html", {"nearest_doctors": nearest_doctors})


def search_nearest_pharmacy(request):
    # Retrieve user location from session
    user_lat = request.session.get("latitude")
    user_lon = request.session.get("longitude")

    # If location is missing, redirect to home or request location
    if user_lat is None or user_lon is None:
        messages.error(
            request, "Your location is required to find nearby pharmacies.")
        return redirect("main_home1")

    # Retrieve all pharmacies
    pharmacies = Pharmacy.objects.all()
    nearest_pharmacies = []

    for pharmacy in pharmacies:
        # Ensure pharmacy has valid latitude & longitude
        if pharmacy.latitude is None or pharmacy.longitude is None:
            continue  # Skip this pharmacy if location is missing

        # Calculate distance using Haversine formula
        distance = haversine(float(user_lat), float(user_lon), float(
            pharmacy.latitude), float(pharmacy.longitude))

        nearest_pharmacies.append({
            "pharmacy": pharmacy,
            "distance": distance
        })

    # Sort pharmacies by distance (nearest first)
    nearest_pharmacies.sort(key=lambda x: x["distance"])

    return render(request, "main_app/search-nearest-pharmacy.html", {"nearest_pharmacies": nearest_pharmacies})


def search_nearest_medical_facility(request):
    # Retrieve user location from session
    user_lat = request.session.get("latitude")
    user_lon = request.session.get("longitude")

    # If location is missing, redirect to home or request location
    if user_lat is None or user_lon is None:
        messages.error(
            request, "Your location is required to find nearby medical facilities.")
        return redirect("main_home1")

    # Retrieve all medical facilities
    medical_facilities = MedicalPhacility.objects.all()
    nearest_medical_facilities = []

    for facility in medical_facilities:
        # Ensure facility has valid latitude & longitude
        if facility.latitude is None or facility.longitude is None:
            continue  # Skip this facility if location is missing

        # Calculate distance using Haversine formula
        distance = haversine(float(user_lat), float(user_lon), float(
            facility.latitude), float(facility.longitude))

        nearest_medical_facilities.append({
            "facility": facility,
            "distance": distance
        })

    # Sort medical facilities by distance (nearest first)
    nearest_medical_facilities.sort(key=lambda x: x["distance"])

    return render(request, "main_app/search-nearest-medical-facility.html", {"nearest_medical_facilities": nearest_medical_facilities})


def search_nearest_nurse(request):
    # Retrieve user location from session
    user_lat = request.session.get("latitude")
    user_lon = request.session.get("longitude")

    # If location is missing, redirect to home or request location
    if user_lat is None or user_lon is None:
        messages.error(
            request, "Your location is required to find nearby nurses.")
        return redirect("main_home1")

    # Retrieve all nurses
    nurses = Nurse.objects.all()
    nearest_nurses = []

    for nurse in nurses:
        # Ensure nurse has valid latitude & longitude
        if nurse.latitude is None or nurse.longitude is None:
            continue  # Skip this nurse if location is missing

        # Calculate distance using Haversine formula
        distance = haversine(float(user_lat), float(
            user_lon), float(nurse.latitude), float(nurse.longitude))

        nearest_nurses.append({
            "nurse": nurse,
            "distance": distance
        })

    # Sort nurses by distance (nearest first)
    nearest_nurses.sort(key=lambda x: x["distance"])

    return render(request, "main_app/search-nearest-nurse.html", {"nearest_nurses": nearest_nurses})


# views.py


@csrf_exempt  # If using POST without Ajax, ensure CSRF is handled
def save_location(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        if latitude and longitude:
            request.session["latitude"] = latitude
            request.session["longitude"] = longitude
            request.session["location_shared"] = "true"

    return redirect("main_home1")  # Redirect to index after storing


# Haversine formula to calculate distance between two points on the Earth
