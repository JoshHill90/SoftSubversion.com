from django.forms.models import BaseModelForm 
from django.http import JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from pathlib import Path
from .models import Billing
from clients.models import Client
from .forms import RegForm, ProfileForm, LoginForm
from gallery.models import Image, Print, Project
from clients.models import Client
from django.shortcuts import render, redirect
import os
import json
import requests

def clientJsonData(jsonDataSets):

    json_filename = 'clientData.json'
    
    for static_dir in settings.STATICFILES_DIRS:
        json_path = os.path.join(static_dir, 'json', json_filename)
        json_directory = os.path.dirname(json_path)
        
        Path(json_directory).mkdir(parents=True, exist_ok=True)
    
    with open(json_path, "w") as json_writer:
        json.dump(jsonDataSets, json_writer) 
        
def invoiceDetailsJson(jsonDataSets):

    json_filename = 'invoiceDetails.json'
    
    for static_dir in settings.STATICFILES_DIRS:
        json_path = os.path.join(static_dir, 'json', json_filename)
        json_directory = os.path.dirname(json_path)
        
        Path(json_directory).mkdir(parents=True, exist_ok=True)
    
    with open(json_path, "w") as json_writer:
        json.dump(jsonDataSets, json_writer) 
        
        

#-------------------------------------------------------------------------------------------------------#
# Billing views
#-------------------------------------------------------------------------------------------------------#

def billing_panel(request):
    client_list = Client.objects.all()
    image_list = Image.objects.all()
    billing_info = Billing.objects.all()
    project_list = Project.objects.all()
    project_invoice = ['']
    project_invoice.clear()
    bal_due = 0
    bal_paid = 0
    bal_ern = 0
    
    # Get query parameters
    project_query = request.GET.get('project')
    client_query = request.GET.get('client')
    number_query = request.GET.get('number')
    completed_query = request.GET.get('fufiled')
    order_set = request.GET.get('order')

    # Calculate balances
    bills = Billing.objects.all()
    for bill in bills:
        if not bill.fufiled:
            bal_due += bill.billed
            bal_paid += bill.paid
            bal_out = bal_due - bal_paid
        else:
            bal_ern += bill.paid

    # Initial query set
    billing_info = Billing.objects.all()

    # Apply filters
    if project_query:
        billing_info = billing_info.filter(Q(project_id__name=project_query))
    if client_query:
        billing_info = billing_info.filter(Q(client_id__name=client_query))
    if number_query:
        billing_info = billing_info.filter(Q(invoice__icontains=number_query))

    # Apply completion status filter
    if completed_query == 'open':
        billing_info = billing_info.filter(Q(fufiled=False))
    elif completed_query == 'closed':
        billing_info = billing_info.filter(Q(fufiled=True))
        
    if order_set == 'Oldest':
        billing_info = billing_info.order_by('id')
    else:
        billing_info = billing_info.order_by('-id')
        
    # billing details set  
    for bill in billing_info:
        client_billed = str(bill.client_id)    
        for project in project_list:
            if project.id == bill.project_id.id:
                project_images = []
                for image in image_list:
                    if image.project_id == project:
                        image_set = {'imageID': image.id, 'ImageTitle': image.title}
                        project_images.append(image_set)
                project_details = {
                    "project": project.name, 
                    'invoice': bill.invoice,
                    'billed': bill.billed,
                    'paid': bill.paid,
                    'client': client_billed,
                    'images': project_images,
                                }
                project_invoice.append({'billID': bill.id, 'project_details': project_details})
                
    return render(request, 'billing/billing.html', 
                  {
                      'invoice': project_invoice,
                      'totalDue': bal_due,
                      'totalPaid': bal_paid,
                      'totalEarned': bal_ern,
                      'outstanding': bal_out,
                      'project_list': project_list,
                      'client_list': client_list
        })          
                
class BillCreateView(CreateView):
    template_name = 'billing/billing-create.html'
    model = Billing
    
    def form_valid(self, form):
        self.object = form.save()
        obj_bill = self.object
        
        system_id = obj_bill.id
        invc_num = "BIN:" + str(system_id)
        obj_bill.invoice = invc_num
        obj_bill.save()
        
        return redirect('billing-details', system_id)

class BillEditView(UpdateView):
    model = Billing
    template_name = 'billing/billing-edit.html'
    success_url = reverse_lazy('billing')

class BillDeleteView(DeleteView):
    model = Billing
    template_name = 'billing/billing-delete.html'
    success_url = reverse_lazy('billing')
    
    
def billing_details(request, id):
    invoice = Billing.objects.get(id=id)
    
        # Calculate balances

    bal_due = float(invoice.billed)

    bal_paid = float(invoice.paid)

    bal_due_ratio = (bal_paid / bal_due)* 100
    bal_due_ratio = int(bal_due_ratio)
    print(bal_due_ratio)
    
    if bal_due != bal_paid:
        bal_out = bal_due - bal_paid
    else:
        bal_out = 0
        

    return render(request, 'billing/billing-details.html', {'invoice':invoice,
                                                            'due': bal_due,
                                                            'paid': bal_paid,
                                                            'ratio':bal_due_ratio,
                                                            'out': bal_out
                                                            })

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
    client_images = Image.objects.exclude(Q(client_id="1"))
    
    # setting up JSON string
    client_images_list = {}
    site_image_count = len(site_image)
    client_image_count = len(client_images)
    print_list_count = len(print_list)
    image_list_count = len(image_list)
    total_Image_count = image_list_count + print_list_count
    
    site_Image_data = {'siteImageCount': site_image_count}
    client_Image_data = {'clientImageCount': client_image_count}
    print_Image_data = {'printImageCount': print_list_count}
    total_Image_data = {'totalImageCount': total_Image_count}
    for client in client_list:
        client_images_count = 0
        for image in image_list:
            if image.client_id == client:
                client_images_count +=1
        client_images_list[client.id] = {
            "clientsName": client.name,
            "clientsCount": client_images_count
            }
    jsonDataSets = {
        'clientImageList': client_images_list,
        'site_Image_data': site_Image_data,
        'client_Image_data': client_Image_data,
        'print_Image_data': print_Image_data,
        'total_Image_data': total_Image_data
    }
    clientJsonData(jsonDataSets)

    

    return render(request, 'management/main.html', {
        'image_list': image_list,
        'print_list': print_list,
        'project_list': project_list,
        'client_list': client_list,
        'gal1': gal1,
        'gal2': gal2,
        'gal4': gal4,
        'site_image': site_image,
        'client_images':client_images,
    })
    