from base.models import Governorate, Specialization, MedicalType


def global_data(request):
    return {
        'governorates': Governorate.objects.all(),
        'specializations': Specialization.objects.all(),
        'medical_types': MedicalType.objects.all(),
    }
