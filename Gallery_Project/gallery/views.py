from typing import Any, Dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Image, Print, Project
from clients.models import ProjectRequest
from .forms import ImageForms, PrintForms, ProjectForms, CreatImageForm
from Gallery_Project.env.app_Logic.photo_layer import col3_col6_col3
from Gallery_Project.env.cloudflare_API.CFAPI import APICall, Encode_Metadata
from django.core.paginator import Paginator 
from Gallery_Project.env.app_Logic.json_utils import DataSetUpdate

data_triggere = DataSetUpdate()

#-----------------------------------------------------------------------------------------------------------#
#
# functions
#
#-----------------------------------------------------------------------------------------------------------#
def append_cloundflare_id(cf_id, image_id, type_image):
    if type_image == 'print':
        update_image_record = Print.objects.get(id=image_id)
    elif type_image =='image':
        update_image_record = Image.objects.get(id=image_id)
    
    image_url = 'https://imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/' + cf_id +'/display'
    update_image_record.image_link = image_url
    update_image_record.save()
    
#-------------------------------------------------------------------------------------------------------#
# gallery column sorter
#-------------------------------------------------------------------------------------------------------#

def column_sort(image_list):
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

    return image_col1, image_col2, image_col3, new_list, len1, len2


#-----------------------------------------------------------------------------------------------------------#
#
# views
#
#-----------------------------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------------------------#
# gallery views site and client
#-------------------------------------------------------------------------------------------------------#

def gallery_hall(request):
    image_list = Image.objects.all()
    print_list = Print.objects.all()

    return render(request, 'gallery/gallery.html', {
        'image_list': image_list,
        'print_list': print_list
    })

def model_gallery(request):
    image_list = Image.objects.filter(Q(display="subgal1") | Q(display="gallery1"))
    image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)

    return render(request, 'gallery/model-gallery.html', {
        'image_list': image_list,
        'image_col1': image_col1,
        'image_col2': image_col2,
        'image_col3': image_col3,
        'new_list': new_list,
        'len1': len1,
        'len2': len2,
    })

def wedding_gallery(request):
    image_list = Image.objects.filter(Q(display="subgal2") | Q(display="gallery2"))
    image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)

    return render(request, 'gallery/wedding-gallery.html', {
        'image_list': image_list,
        'image_col1': image_col1,
        'image_col2': image_col2,
        'image_col3': image_col3,
        'new_list': new_list,
        'len1': len1,
        'len2': len2,
    })

def prints_gallery(request):
    image_list = Print.objects.filter(Q(display="subgal3") | Q(display="gallery3"))
    image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)

    return render(request, 'gallery/prints-gallery.html', {
        'image_list': image_list,
        'image_col1': image_col1,
        'image_col2': image_col2,
        'image_col3': image_col3,
        'new_list': new_list,
        'len1': len1,
        'len2': len2,
    })

def family_gallery(request):
    image_list = Image.objects.filter(Q(display="subgal4") | Q(display="gallery4"))
    image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)

    return render(request, 'gallery/family-gallery.html', {
        'image_list': image_list,
        'image_col1': image_col1,
        'image_col2': image_col2,
        'image_col3': image_col3,
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_pk = self.kwargs['pk']
        try:
            query_previous_image = Image.objects.filter(pk__lt=current_pk).order_by('-pk').first()
            previous_image = query_previous_image.id
        except AttributeError:
            previous_image = ''
        
        try:
            query_next_image = Image.objects.filter(pk__gt=current_pk).order_by('pk').first()
            next_image = query_next_image.id
        except AttributeError:
            next_image = ''

        context['previous_image'] = previous_image
        context['next_image'] = next_image
        
        return context
    

#-------------------------------------------------------------------------------------------------------#
# Prints views
#-------------------------------------------------------------------------------------------------------#

class PrintListView(ListView):
    template_name = 'gallery/prints/prints.html'
    data_triggere.json_chart_data()
    model = Print

class PrintEditView(UpdateView):
    model = Print
    form_class = PrintForms
    template_name = 'gallery/prints/print-edit.html'

class PrintDeleteView(DeleteView):
    model = Print
    template_name = 'gallery/prints/print-delete.html'
    success_url = reverse_lazy('print')
    
class PrintDetailView(DetailView):
    model = Print
    form_class = PrintForms
    template_name = 'gallery/prints/print-details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_pk = self.kwargs['pk']
        try:
            query_previous_print = Print.objects.filter(pk__lt=current_pk).order_by('-pk').first()
            previous_image = query_previous_print.id
        except AttributeError:
            previous_image = ''
        
        try:
            query_next_print = Print.objects.filter(pk__gt=current_pk).order_by('pk').first()
            next_image = query_next_print.id
        except AttributeError:
            next_image = ''

        context['previous_image'] = previous_image
        context['next_image'] = next_image
        
        return context

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


def upload_image(request):
    api = APICall()
    encode = Encode_Metadata()
    multi_encode_bond = encode.direct_request_encoder()
    cloudflare_id = api.auth_direct_upload(multi_encode_bond)
    cloudflare_id = str(cloudflare_id)
    front_end_url = f'https://upload.imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/{cloudflare_id}'

    return render(request, 'gallery/image/image-upload.html',
                  {
                      'front_end_url': front_end_url,
                      'clfr_id': cloudflare_id}
                  )
    
class CreateImage(CreateView):
    model = Image
    form_class = CreatImageForm
    template_name = 'gallery/image/image-create.html'
    type_image = 'image'

    def form_valid(self, form):
        self.object = form.save()
        cf_id = form.cleaned_data.get('cloudflare_id',)
        image_id = self.object.id
        append_cloundflare_id(cf_id, image_id, self.type_image)
        title = form.cleaned_data.get('title', )
        tag = form.cleaned_data.get('tag', )
        private = form.cleaned_data.get('private', )
        display = form.cleaned_data.get('display', )
        aspect  = form.cleaned_data.get('aspect', )
        client_id  = form.cleaned_data.get('client_id', )
        client_id_str = str(client_id)
        project_id = form.cleaned_data.get('project_id', )
        project_id_str = str(project_id.name)
        silk_id = self.object.silk_id
        metadata_push = [
                title,  
                tag,
                private, 
                display, 
                aspect, 
                client_id_str, 
                project_id_str,
                cf_id,
                silk_id,
        ]
        api = APICall()
        api.image_update(metadata_push, cf_id, self.type_image)
        return redirect('image-details', image_id)
    
    
class PrintCreateView(CreateView):
    model = Print
    form_class = PrintForms
    template_name = 'gallery/prints/print-create.html'
    type_image = 'print'
    def form_valid(self, form):
        self.object = form.save()
        cf_id = form.cleaned_data.get('cloudflare_id',)
        image_id = self.object.id
        append_cloundflare_id(cf_id, image_id, self.type_image)
        title = form.cleaned_data.get('title', )
        cost = form.cleaned_data.get('tag', )
        details = form.cleaned_data.get('details', )
        status = form.cleaned_data.get('status', )
        display = form.cleaned_data.get('display', )
        aspect  = form.cleaned_data.get('aspect', )
        silk_id = self.object.silk_id
        metadata_push = [
                title,
                cost,
                details,
                status,
                display, 
                aspect, 
                cf_id,
                silk_id,
        ]
        api = APICall()
        api.image_update(metadata_push, cf_id, self.type_image)
        return redirect('print-details', image_id)