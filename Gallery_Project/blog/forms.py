from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'user', 'article', 'preview', 'tag', 'image_id')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'userName', 'type': 'hidden'}),
            'article': forms.Textarea(attrs={'class': 'form-control'}),
            'preview' : forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.Textarea(attrs={'class': 'form-control'}),
            'image_id': forms.Select(attrs={'class': 'form-control'})
        }

