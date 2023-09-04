from django.forms.models import BaseModelForm 
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from pathlib import Path
from .models import Client, Invite
from .forms import ClientForm, InviteForm
#from .forms import 
from gallery.models import Image, Project
from management.models import Payments, Billing
from django.shortcuts import render, redirect
import os
import json
import secrets

def hex_gen():
    random_hex = secrets.token_hex(16)
    print(random_hex)
    return str(random_hex)
 
def client_main(request):
    client_list = Client.objects.exclude(Q(id='1'))
    client_images = Image.objects.exclude(Q(client_id="1"))
    project_list = Project.objects.exclude(Q(user_id="1"))
    project_temp = 0
    image_temp = 0
	# Get query parameters
    project_query = request.GET.get('project')
    client_query = request.GET.get('client')
    order_set = request.GET.get('order')

    # Apply filters
    if project_query:
        project_list = project_list.filter(Q(name__icontains=project_query))
        project_ids = project_list.values_list('id',)
        client_list = client_list.filter(user_id__in=project_ids)

    if client_query:
        client_list = client_list.filter(Q(name__icontains=client_query))
        
	        
    if order_set == 'Oldest':
        client_list = client_list.order_by('id')
    else:
        client_list = client_list.order_by('-id')
   
    clients_info =[]
    for client in client_list:
        client_details = {'client': client.name, 'client_id': client.id, 'client_user': client.user_id}
        for project in project_list:
            if client.user_id == project.user_id:
                project_temp +=1
                for image in client_images:
                    if image.client_id.id == client.id and image.project_id.id == project.id:
                        image_temp +=1
        clients_info.append({'client_details': client_details, 'project_count': project_temp, 'image_count': image_temp})
    print(clients_info)
                	
    return render(request, 'client/client.html', {
		'client_info': clients_info,
		'client_images':client_images,
		'project_list': project_list
	})
    

def client_details(request, client_id):
    client_info = Client.objects.filter(id=client_id)

    return render(request, 'client/client-details.html', {
		'client_info': client_info,
  })
    
class ClientCreate(CreateView):
    form_class = ClientForm
    model = Client
    template_name = 'client/client-create.html'

class ClientIntake(CreateView):
    form_class = InviteForm
    model = Invite
    template_name = 'client/client-invite.html'
    
    def form_valid(self, form):
        self.object = form.save()
        email = form.cleaned_data.get('email',)
        name = form.cleaned_data.get('email',)
        hex_key = hex_gen()
        print(hex_key)
        add_feild = self.object
        add_feild.hexkey = hex_key
        add_feild.save()
        
        
        return redirect('login')
    
#---------#


def project_binder(request, id):
    users_id = id
    client = Client.objects.filter(Q(user_id=users_id))
    client_id = Client.objects.get(user_id=users_id)
    client_images = Image.objects.filter(Q(client_id=client_id))
    project_list = Project.objects.filter(Q(user_id__id=users_id))
                	
    return render(request, 'client-portal/project-binder.html', {
		'client_info': client,
		'client_images':client_images,
		'project_list': project_list
	})