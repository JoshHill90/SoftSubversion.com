from django import forms
from .models import Client
from phonenumber_field.modelfields import PhoneNumberField

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'phone', 'email', 'user_id', 'group_id')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_id': forms.Select(attrs={'class': 'form-control', 'value': '', 'id': 'userName', 'type': 'hidden'}),
            'group_id': forms.Select(attrs={'class': 'form-control'})
        }