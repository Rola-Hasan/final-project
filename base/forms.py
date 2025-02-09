from .models import UserProfile
from django import forms
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'firstname', 'lastname', 'gender', 'specialization',
            'insurancecompany', 'phone_number', 'governorate', 'address'
        ]
        labels = {
            'firstname': 'الاسم الأول',
            'lastname': 'الاسم الأخير',
            'gender': 'الجنس',
            'specialization': 'الاختصاص',
            'insurancecompany': 'شركة التأمين',
            'phone_number': 'رقم الهاتف',
            'governorate': 'المحافظة',
            'address': 'العنوان',
        }
        widgets = {
            'gender': forms.Select(choices=[('M', 'ذكر'), ('F', 'أنثى')]),
            'specialization': forms.Select(attrs={'class': 'form-select'}),
            'insurancecompany': forms.Select(attrs={'class': 'form-select'}),
            'governorate': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'أدخل عنوانك هنا',
                'class': 'form-control'
            }),
        }


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         # Include other fields if needed
#         fields = ['username', 'profile_picture']
