from django import forms
from .models import Client, Invite, ProjectRequest, RequestReply, ProjectTerms
from phonenumber_field.modelfields import PhoneNumberField

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ('name', 'date', 'scope', 'details', 'location')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'scope': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
        }
        
class RequestReplyComment(forms.ModelForm):
    class Meta:
        model = RequestReply
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProjectTermsForm(forms.ModelForm):
    class Meta:
        model = ProjectTerms
        fields = ('project_cost',
                  'deposit',
                  'location',
                  'city',
                  'state',
                  'zip',
                  'session_date1',
                  'session_start1',
                  'session_end1',
                  
                  'session_date2',
                  'session_start2',
                  'session_end2',
                  
                  'session_date3',
                  'session_start3',
                  'session_end3',
                  
                  'session_date4',
                  'session_start4',
                  'session_end4',
                  'services'
                  )
        
        widgets = {
            'project_cost': forms.TextInput(attrs={'class': 'form-control'}),
            'deposit': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zip': forms.TextInput(attrs={'class': 'form-control'}),
            'session_date1': forms.DateInput(attrs={'class': 'form-control'}),
            'session_start1': forms.TimeInput(attrs={'class': 'form-control'}),
            'session_end1': forms.TimeInput(attrs={'class': 'form-control'}),
            
            'session_date2': forms.DateInput(attrs={'class': 'form-control'}),
            'session_start2': forms.TimeInput(attrs={'class': 'form-control'}),
            'session_end2': forms.TimeInput(attrs={'class': 'form-control'}),
            
            'session_date3': forms.DateInput(attrs={'class': 'form-control'}),
            'session_start3': forms.TimeInput(attrs={'class': 'form-control'}),
            'session_end3': forms.TimeInput(attrs={'class': 'form-control'}),
            
            'session_date4': forms.DateInput(attrs={'class': 'form-control'}),
            'session_start4': forms.TimeInput(attrs={'class': 'form-control'}),
            'session_end4': forms.TimeInput(attrs={'class': 'form-control'}),
            
            'services': forms.Textarea(attrs={'class': 'form-control'}),




        }