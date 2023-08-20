from django import forms
from .models import Image, Print, Project

class ImageForms(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title','tag', 'private', 'display', 'aspect', 'client_id', 'project_id','cloudflare_id')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'private': forms.CheckboxInput(attrs={'type': 'checkbox',
                                                  'class': 'form-check-input',
                                                  'id': 'flexSwitchCheckChecked',
                                                  }),
            'display': forms.Select(attrs={'class': 'form-control'}), 
            'aspect': forms.Select(attrs={'class': 'form-control'}),                                       
            'client_id': forms.Select(attrs={'class': 'form-control'}),
            'project_id': forms.Select(attrs={'class': 'form-control'}),
            'cloudflare_id': forms.TextInput(attrs={'class': 'form-control'}),                              
        }

class PrintForms(forms.ModelForm):
    class Meta:
        model = Print
        fields = ('title','cost', 'details', 'status', 'display', 'aspect', 'cloudflare_id')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'type': 'checkbox',
                                                  'class': 'form-check-input',
                                                  'id': 'flexSwitchCheckChecked',
                                                  }),
            'display': forms.Select(attrs={'class': 'form-control'}),
            'aspect': forms.Select(attrs={'class': 'form-control'}),      
            'cloudflare_id': forms.TextInput(attrs={'class': 'form-control', 'id': "cloudflare_id", 'style': 'display: none;'}),                         
        }

class ProjectForms(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'cost', 'status', 'user_id')
        widget ={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'client_id': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'type': 'checkbox',
                                                  'class': 'form-check-input',
                                                  'id': 'flexSwitchCheckChecked',
                                                  }),
            'user_id': forms.TextInput(attrs={'class': 'form-control'})  
        }
        
class CreatImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title','tag', 'private', 'display', 'aspect', 'client_id', 'project_id' ,'cloudflare_id')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'private': forms.CheckboxInput(attrs={'type': 'checkbox',
                                                  'class': 'form-check-input',
                                                  'id': 'flexSwitchCheckChecked',
                                                  }),
            'display': forms.Select(attrs={'class': 'form-control'}), 
            'aspect': forms.Select(attrs={'class': 'form-control'}),                                       
            'client_id': forms.Select(attrs={'class': 'form-control'}),
            'project_id': forms.Select(attrs={'class': 'form-control'}),
            'cloudflare_id': forms.TextInput(attrs={'class': 'form-control', 'id': "cloudflare_id", 'style': 'display: none;'}),                              
        }