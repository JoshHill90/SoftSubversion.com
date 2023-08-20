from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import RegForm, ProfileForm, LoginForm
from gallery.models import Image, Print, Project
from clients.models import Client


#-------------------------------------------------------------------------------------------------------#
# Registration views
#-------------------------------------------------------------------------------------------------------#

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeView
    template_name = 'registration/change-password.html'
    success_url = reverse_lazy('index')


class UserEditView(generic.UpdateView):
    form_class = ProfileForm
    template_name = 'registration/edit-profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, *args):
        return self.request.user
    

class UserRegistrationView(generic.CreateView):
    form_class = RegForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')


class UserLoginView(generic.CreateView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')
    

#-------------------------------------------------------------------------------------------------------#
# Management view
#-------------------------------------------------------------------------------------------------------#

def o_main(request):
    image_list = Image.objects.all()
    print_list = Print.objects.all()
    project_list = Project.objects.all()
    client_list = Client.objects.all()
    gal1 = Image.objects.filter(Q(display="subgal1") | Q(display="gallery1"))
    gal2 = Image.objects.filter(Q(display="subgal2") | Q(display="gallery2"))
    gal4 = Image.objects.filter(Q(display="subgal4") | Q(display="gallery4"))
    site_image = Image.objects.filter(Q(client_id="1"))
    client_images = Image.objects.exclude(Q(client_id=1))
    
    

    return render(request, 'management/main.html', {
        'image_list': image_list,
        'print_list': print_list,
        'project_list': project_list,
        'client_list': client_list,
        'gal1': gal1,
        'gal2': gal2,
        'gal4': gal4,
        'site_image': site_image,
        'client_images':client_images
    })