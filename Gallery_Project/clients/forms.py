from django import forms
from .models import Client
from phonenumber_field.modelfields import PhoneNumberField

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('title', 'author', 'article', 'preview', 'category', 'image_url')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': PhoneNumberField(),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'project_id' : forms.Select(attrs={'class': 'form-control'}),
            'user_id': forms.Select(attrs={'class': 'form-control', 'value': '', 'id': 'userName', 'type': 'hidden'}),
            'group_id': forms.Select(attrs={'class': 'form-control'})
        }