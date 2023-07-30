from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Image, Print, Project
from .forms import ImageForms, PrintForms, ProjectForms


def gallery_hall(request):
    image_list = Image.objects.all()
    print_list = Print.objects.all()

    return render(request, 'gallery/gallery.html', {
        'image_list': image_list,
        'print_list': print_list
    })



#-------------------------------------------------------------------------------------------------------#
# Image views
#-------------------------------------------------------------------------------------------------------#

class ImageListView(ListView):
    template_name = 'gallery/image/images.html'
    model = Image
    
class ImageCreateView(CreateView):
    model = Image
    form_class = ImageForms
    template_name = 'gallery/image/image-create.html'

def image_upload(request):
    pass

class ImageEditView(UpdateView):
    model = Image
    form_class = ImageForms
    template_name = 'gallery/image/image-edit.html'

class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'gallery/image/image-delete.html'
    success_url = reverse_lazy('images')

class ImageDetailView(DetailView):
    model = Image
    form_class = ImageForms
    template_name = 'gallery/image/image-details.html'

#-------------------------------------------------------------------------------------------------------#
# Prints views
#-------------------------------------------------------------------------------------------------------#

class PrintListView(ListView):
    template_name = 'gallery/print/prints.html'
    model = Print
    
class PrintCreateView(CreateView):
    model = Print
    form_class = PrintForms
    template_name = 'gallery/print/print-create.html'

class PrintEditView(UpdateView):
    model = Print
    form_class = PrintForms
    template_name = 'gallery/print/print-edit.html'

class PrintDeleteView(DeleteView):
    model = Print
    template_name = 'gallery/print/print-delete.html'
    success_url = reverse_lazy('print')
    
class PrintDetailView(DetailView):
    model = Print
    form_class = PrintForms
    template_name = 'gallery/print/print-details.html'

def print_upload(request):
    pass

#-------------------------------------------------------------------------------------------------------#
# Prints views
#-------------------------------------------------------------------------------------------------------#

class ProjectListView(ListView):
    template_name = 'gallery/project/projects.html'
    model = Project
    
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForms
    template_name = 'gallery/project/project-create.html'

class ProjectEditView(UpdateView):
    model = Project
    form_class = ProjectForms
    template_name = 'gallery/project/project-edit.html'

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'gallery/project/project-delete.html'
    success_url = reverse_lazy('print')
    
class ProjectDetailView(DetailView):
    model = Project
    form_class = ProjectForms
    template_name = 'gallery/project/project-details.html'