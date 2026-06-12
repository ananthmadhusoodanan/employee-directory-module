from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee

        fields = [
    'Full_Name',
    'Department',
    'Email',
    'Phone_Number',
    'Designation',
    'Status',
    'Date_Joined',
    'img'
]
        widgets = {
            'Date_Joined': forms.DateInput(attrs={
                'type': 'date'
            })
        }