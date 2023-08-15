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
from Gallery_Project.env.app_Logic.photo_layer import col3_col6_col3


def gallery_hall(request):
    image_list = Image.objects.all()
    print_list = Print.objects.all()

    return render(request, 'gallery/gallery.html', {
        'image_list': image_list,
        'print_list': print_list
    })

def model_gallery(request):
    image_list = Image.objects.all()
    image_inline = []
    image_col1 = []
    image_col2 = []
    image_col3 = []

    for image in image_list:
        new_list = []
        image_inline.append([image.id, image.aspect])

    image_list1, image_list2, image_list3 = col3_col6_col3 (image_inline)
    for image in image_list:
        for image1 in image_list1:
            if image.id in image1:
                image_col1.append(image)
                
        for image2 in image_list2:
            if image.id in image2:
                image_col2.append(image)

        for image3 in image_list3:
            if image.id in image3:
                image_col3.append(image)

    len1 = len(image_col1)
    len2 = len(image_col2)+len1
    for listed_item in image_col1 + image_col2 + image_col3:
        new_list.append(listed_item)

    return render(request, 'gallery/model-gallery.html', {
        'image_list': image_list,
        'image_col1': image_col1,
        'image_col2': image_col2,
        'image_col3': image_col3,
        'new_list': new_list,
        'len1': len1,
        'len2': len2,
    })

def prints_gallery(request):
    print_list = Print.objects.all()
    print_inline = []
    print_col1 = []
    print_col2 = []
    print_col3 = []

    for print in print_list:
        new_list = []
        print_inline.append([print.id, print.aspect])

    print_list1, print_list2, print_list3 = col3_col6_col3 (print_inline)
    for print in print_list:
        for print1 in print_list1:
            if print.id in print1:
                print_col1.append(print)
                
        for print2 in print_list2:
            if print.id in print2:
                print_col2.append(print)

        for print3 in print_list3:
            if print.id in print3:
                print_col3.append(print)

    len1 = len(print_col1)
    len2 = len(print_col2)+len1
    for listed_item in print_col1 + print_col2 + print_col3:
        new_list.append(listed_item)
    

    return render(request, 'gallery/prints-gallery.html', {
        'print_list': print_list,
        'print_col1': print_col1,
        'print_col2': print_col2,
        'print_col3': print_col3,
        'new_list': new_list,
        'len1': len1,
        'len2': len2,
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

#---------------------------------------------------------------------------------------------------------#
