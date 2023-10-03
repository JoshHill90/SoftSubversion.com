from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Image, Print, Project, ProjectEvents
from clients.models import ProjectRequest, RequestReply
from .forms import ImageForms, PrintForms, ProjectForms, CreatImageForm, ProjectEventForms
from clients.forms import ProjectTermsForm
from Gallery_Project.env.app_Logic.photo_layer import col3_col6_col3
from Gallery_Project.env.cloudflare_API.CFAPI import APICall, Encode_Metadata
from django.core.paginator import Paginator 
from Gallery_Project.env.app_Logic.json_utils import DataSetUpdate
from clients.models import Client, ProjectRequest, ProjectTerms
from management.models import Payments, Billing
from datetime import datetime
import calendar
from Gallery_Project.env.app_Logic.date_time_calendar import cal_gen, date_passed_check
import datetime
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
    new_list = []

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

#-------------------------------------------------------------------------------------------------------#
# Prints views
#-------------------------------------------------------------------------------------------------------#


def project_main(request):
    client_list = Client.objects.exclude(Q(name='Soft Subversion'))
    project_images = Image.objects.exclude(Q(client_id__name="Soft Subversion"))
    project_list = Project.objects.exclude(Q(name="Soft Subversion"))
    project_request = ProjectRequest.objects.all()
    project_events = ProjectEvents.objects.all()
    project_temp = 0
    image_temp = 0
    client_name = ''
    
	# Get query parameters
    project_query = request.GET.get('project')
    client_query = request.GET.get('client')
    order_set = request.GET.get('order')
    



    month0, month1, month2, cal, year, todays_date, cal_date = cal_gen()
    # Apply filters
    if project_query:
        project_list = project_list.filter(Q(name__icontains=project_query))


    if client_query:
        client_list = client_list.filter(Q(name__icontains=client_query))
        #client_ids = client_list.values_list('id',)
        #project_list = project_list.filter(user_id__in=client_ids)
	        
    if order_set == 'Oldest':
        project_list = project_list.order_by('id')
    else:
        project_list = project_list.order_by('-id')
   
    project_info =[]
    for project in project_list:

            
        client_name = str(project.user_id.first_name + ' ' + project.user_id.last_name)
        project_details = {
            'project': project.name,
            'project_id': project.id,
            'project_client': client_name,
            'project_status': project.status
                           }
        
        for image in project_images:
            if image.project_id.id == project.id:
                image_temp +=1
        project_info.append({'project_details': project_details, 'image_count': image_temp})
                	
    return render(request, 'gallery/project/projects.html', {
		'project_info': project_info,
		'project_images':project_images,
		'project_list': project_list,
        'project_request': project_request,
        'project_events': project_events,
        'year': year,
        'month': month1,
        'cal': cal
	})
    
    
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
    
def project_owner_view(request, pk):
    project = Project.objects.get(Q(id=pk))
    project_events = ProjectEvents.objects.filter(project_id=project).order_by('date')
    project_terms = ProjectTerms.objects.get(Q(project_id__id=pk))
    client = Client.objects.get(user_id=project.user_id)
    billing_info = Billing.objects.get(project_id=project)
    payment_list = Payments.objects.filter(billing_id=billing_info)
    images = Image.objects.filter(project_id=project)
    
    active_nodes = 0
    project_progress = []
    for event in project_events:

         # deposit/consulation check
        if event.payment_id and event.event_type == "Deposit Reminder":
            for payment in payment_list:
                if payment.receipt == 'Deposit Cost' and payment == event.payment_id:
                    deposit = '$' + str(payment.amount) + ' Due ' + str(payment.due_date)
                    project_progress.append(deposit)
                    if payment.status == 'paid':
                        active_nodes +=1

                            
        # event check without payment   
        if not event.payment_id:
            event_type = str(event.event_type) + ' on ' + str(event.date)
            project_progress.append(event_type)
            event_passed = date_passed_check(event.date)
            if event_passed == True:
                active_nodes +=1
                                     
        # event check with payment check
        if event.payment_id and event.event_type == "Other Payment":
            for event_payment in payment_list:
                if event_payment == event.payment_id:
                    payment_due = '$' + str(event_payment.amount)  + ' Due ' +  str(event_payment.due_date)
                    
                    project_progress.append(payment_due)
                    
                    if event_payment.status == 'paid':
                        active_nodes +=1

    
        if event.payment_id and event.event_type == "Project Payment":
            for event_payment in payment_list:
                if event_payment == event.payment_id:
                    project_payment = '$' + str(event_payment.amount) + ' Due ' + str(event_payment.due_date)
                    project_progress.append(project_payment)
                    if event_payment.status == 'paid':
                        active_nodes +=1

                
    print(active_nodes, project_progress)
    return render(request, 'gallery/project/project-details.html', {
        'project': project,
        'project_events': project_events,
        'billing_info': billing_info,
        'payment_list': payment_list,
        'client': client,
        'project_terms': project_terms,
        'project_progress': project_progress,
        'active_nodes': active_nodes,
        "images": images
    })

def project_gallery(request, id):
    project = Project.objects.get(id=id)
    image_list = Image.objects.filter(Q(project_id=project))
    image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)

    return render(request, 'gallery/project/project-gallery/project-gallery.html', {
        'image_list': image_list,
        'image_col1': image_col1,
        'image_col2': image_col2,
        'image_col3': image_col3,
        'new_list': new_list,
        'len1': len1,
        'len2': len2,
    })

def project_notes(request, id):
    project_terms = ProjectTerms.objects.get(project_id=id)
    project_request = ProjectRequest.objects.get(id=project_terms.project_request_id.id)
    request_reply = RequestReply.objects.filter(Q(project_request_id=project_request.id))

    return render(request, 'gallery/project/project-notes.html', {
        'request_reply': request_reply,
        'project_terms':project_terms,
        'project_request': project_request
    })
#---------------------------------------------------------------------------------------------------------#
# Calendar
#---------------------------------------------------------------------------------------------------------#

class ProjectEventsCreate(CreateView):
    model = ProjectEvents
    form_class = ProjectEventForms

    template_name = 'gallery/project/project-events/new-event.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.exclude(name='Soft Subversion')
        return context
    def form_invalid(self, form):
        self.objects = form.save(commit=False)
        date = form.cleaned_data.get('date',)
        form.save()
        year, month, day = str(date).split('-')
        return redirect('project-calendar', year=year, month=month)
    

def clandar(request, year, month):

    event_list = ProjectEvents.objects.all()
    event_list = ProjectEvents.objects.order_by('date')
    try:
        month_number = int(month)
    except ValueError:
        month = month.title()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number) 


    month0, month1, month2, cal, year_new, todays_date, cal_date = cal_gen(month_number, year)
    next_year = year + 1
    last_year = year - 1
    print(year_new)

    return render(request, 'gallery/project/project-events/calendar.html', {
        'year': year,
        'month1': month1,
        'month0':month0,
        'month2' :month2,
        'cal': cal,
        'event_list':event_list,
        'last_year': last_year,
        'next_year': next_year,
        'todays_date': todays_date,
        'cal_date': cal_date
    })
    
class ProjectEventsDetails(DetailView):
    model = ProjectEvents
    template_name = 'gallery/project/project-events/event-details.html' 


#---------------------------------------------------------------------------------------------------------#
# Image upload and creation
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