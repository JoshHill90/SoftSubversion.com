from typing import Any
from django.forms.models import BaseModelForm 
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from pathlib import Path
from .models import Billing, Payments
from clients.models import Client
from .forms import RegForm, ProfileForm, LoginForm, BillingForm, PaymentForm
from gallery.models import Image, Print, Project, ProjectEvents
from clients.models import Client, Invite
from Gallery_Project.env.app_Logic.json_utils import DataSetUpdate 
from datetime import datetime
import json
import secrets
from django.shortcuts import render, redirect, get_object_or_404
import stripe
from pathlib import Path
import os
from dotenv import load_dotenv
from Gallery_Project.env.app_Logic.json_utils import DataSetUpdate
from Gallery_Project.env.app_Logic.MailerDJ import AutoReply
from Gallery_Project.env.app_Logic.stripe.quick_stripe import QuickStripe, DateFunction, Hexer
from log_app.logging_config import logging
import time

qs = QuickStripe()
df = DateFunction()
hexer = Hexer()
smtp_request = AutoReply

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)
stripe.api_key = os.getenv("STRIPE_KEY")



dataQ = DataSetUpdate()

#-------------------------------------------------------------------------------------------------------#
# Billing views
#-------------------------------------------------------------------------------------------------------#

def billing_panel(request):
    client_list = Client.objects.all()
    image_list = Image.objects.all()
    billing_info = Billing.objects.all()
    project_list = Project.objects.exclude(name="Soft Subversion")
    project_invoice = ['']
    project_invoice.clear()
    bal_due = 0
    bal_paid = 0
    bal_ern = 0
    bal_out = 0
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
            bal_paid += bill.paid
    
    billing_totals = {
        'totalDue': bal_due,
        'totalPaid': bal_paid,
        'totalEarned': bal_ern,
        'outstanding': bal_out,
        }


    # Initial query set
    billing_info = Billing.objects.all()

    # Apply filters
    if project_query:
        billing_info = billing_info.filter(project_id__name=project_query)

    if client_query:
        billing_info = billing_info.filter(project_id__client_id__name=client_query)

    if number_query:
        billing_info = billing_info.filter(invoice__icontains=number_query)

    # Apply completion status filter
    if completed_query == 'open':
        billing_info = billing_info.filter(status='open')
    elif completed_query == 'paid':
        billing_info = billing_info.filter(status='paid')
    elif completed_query == 'draft':
        billing_info = billing_info.filter(status='draft')
    elif completed_query == 'void':
        billing_info = billing_info.filter(status='void')
        
    if order_set == 'Oldest':
        billing_info = billing_info.order_by('id')
    else:
        billing_info = billing_info.order_by('-id')
        
    # billing details set  
    for bill in billing_info:
        client_billed = str(bill.project_id.client_id)    
        for project in project_list:
            if project.id == bill.project_id.id:
                project_images = []
                for image in image_list:
                    if image.project_id == project:
                        image_set = {'imageID': image.id, 'ImageTitle': image.title}
                        project_images.append(image_set)
                project_details = {
                    "project": project.name, 
                    'invoice': bill.invoice_id,
                    'billed': bill.billed,
                    'paid': bill.paid,
                    'status': bill.status,
                    'client': client_billed,
                    'images': project_images,
                                }
                project_invoice.append({'billID': bill.id, 'project_details': project_details})


    return render(
        request, 'billing/billing.html', 
        {
            'invoice': project_invoice,
            'billing_totals':billing_totals,
            'project_list': project_list,
            'client_list': client_list
            }
        )          
                
def BillCreateView(request):
    try:
        template_name = 'billing/billing-create.html'
        form_class = BillingForm
        project_list = Project.objects.exclude(name='Soft Subversion')
        model = Billing
        invoice_details = {}
        line_items_cost = {}
        line_items_receipt = {}
        invoice_total = 0
        if request.method == 'POST':
            terms_form = request.POST
        
            if terms_form:
                #lambda converter 
                converted_to_cents = lambda dollar_amount: int(
                    str(
                        '{:.2f}'.format(
                            float(dollar_amount))).replace('.','')
                )
                # pulls request data from the from submitted and creates dicts 
                for key, value in zip(request.POST.keys(), request.POST.values()):
                    if 'line_item_cost' in key:
                        line_items_cost['C' + key[-1]] = value
                        invoice_total += float(value)
                        
                    elif 'line_item_receipt' in key:
                        line_items_receipt['R' + key[-1]] = value
                    else:
                        invoice_details[key] = value

                
                        
                # sets vars for frrom data
                
                selected_project = project_list.get(id=invoice_details.get('project_id'))
                stripe_date = df.date_distance(invoice_details.get('due_date'))
                set_payment_type = invoice_details.get('payment_type')
                set_details = f"{set_payment_type} for photography project:{selected_project.name}"
                
                # Get strip ID from client            
                stripe_id = selected_project.client_id.strip_id
                
                # strip invoice and project billing 
                set_invoice = qs.create_stripe_invoice(stripe_id, stripe_date, set_details)
                new_billing = model.objects.create(
                        project_id=selected_project,
                        invoice_id=set_invoice.id,
                        billed = invoice_total,
                        details=set_details,
                        due_date=df.number_to_days(stripe_date),
                        payment_type=set_payment_type
                )
                # checks for and creates line item and billing payments 
                if line_items_cost:
                    for cost, receipt in zip(line_items_cost.values(), line_items_receipt.values()):
                        
                        stripe_cost = converted_to_cents(cost)
                        set_lineitem = qs.create_stripe_line_item(stripe_cost, receipt, set_invoice, stripe_id)
                        Payments.objects.create(
                            billing_id=new_billing,
                            amount=cost,
                            receipt=receipt,
                            time_stamp=df.date_now(),
                            item_id=set_lineitem.id,
                        )

                        time.sleep(5)
                
                if invoice_details.get('open'):
                    payment_link, invoice_update = qs.send_stripe_invoice(set_invoice.id)
                    new_billing.payment_link = payment_link
                    new_billing.status = invoice_update.status
                    new_billing.save()
                    ProjectEvents.objects.create(
                        title='Deposit Reminder',
                        project_id=selected_project,
                        billing_id=new_billing,
                        date=new_billing.due_date,
                        start=df.payment_time(),
                        end=df.payment_time(),
                        event_type='Payment Reminder',
                        details=f'Event for deposit reminder for project{selected_project}'
                    )

                if invoice_details.get('paidCash'):
                    invoice_update = qs.stripe_cash_payment(set_invoice.id)
                    new_billing.status = invoice_update.status
                    new_billing.paid = invoice_total
                    new_billing.fufiled = True
                    new_billing.save()

                return redirect('billing-details', new_billing.id)
            
        return render(request, template_name, {
            'form_class': form_class,
            'project_list': project_list,
            'model': model
        })
            
    except Exception as e:
        logging.error("Stripe invoice create operation failed: %s", str(e))
        return redirect('issue-backend')

class BillEditView(UpdateView):
    
    model = Billing
    template_name = 'billing/billing-edit.html'
    form_class = BillingForm
        
    def form_valid(self, form):
        try:
            self.object = form.save()
            self.object.save()
            date = form.cleaned_data.get('due_date')
            services = form.cleaned_data.get('details')
            due_date = df.date_distance(date) 
            qs.stripe_update_invoice(self.object.invoice_id, due_date, services)
            success_url = redirect('billing-details', self.object.id)
            return success_url
        except Exception as e:
            logging.error("Stripe invoice update operation failed: %s", str(e))
            return redirect('issue-backend')

class BillDeleteView(DeleteView):
    model = Billing
    template_name = 'billing/billing-delete.html'
    success_url = reverse_lazy('billing')
    
    
def billing_details(request, id):
    invoice = Billing.objects.get(id=id)
    line_items = Payments.objects.filter(billing_id=invoice)
    
    if invoice.billed:
        bal_due = float(invoice.billed)

        bal_paid = float(invoice.paid)

        bal_due_ratio = (bal_paid / bal_due)* 100
        bal_due_ratio = int(bal_due_ratio)
        
        print(bal_due_ratio)
        
        if bal_due != bal_paid:
            bal_out = bal_due - bal_paid
        else:
            bal_out = 0
    else:
        bal_out = 0
        bal_due = 0
        bal_paid = 0
        bal_due_ratio = None
        
    if request.method == 'POST' and 'delete' in request.POST:
        try:
            if invoice.status == "draft":
                qs.delete_stripe_draft(invoice.invoice_id)
                invoice.delete()
                
            if invoice.status =='open':
                void_invoice = qs.void_stripe_invoice(invoice.invoice_id)
                invoice.status = void_invoice.status
                invoice.save()
                
            invoice.delete()
            return redirect('billing')
        
        except Exception as e:
            logging.error("Stripe invoice void operation failed: %s", str(e))
            return redirect('issue-backend')
    if request.method == 'POST' and 'open' in request.POST:
        try:
            if invoice.status == "draft":
                payment_link, invoice_update = qs.send_stripe_invoice(invoice.invoice_id)
                invoice.payment_link = payment_link
                invoice.status = invoice_update.status
                invoice.save()
            if invoice.status =='open':
                qs.resend_invoice(invoice.project_id.user_id,invoice.project_id, invoice)
                
            
            return redirect('billing-details', id=invoice.id)
            
        except Exception as e:
            logging.error("Stripe invoice send operation failed: %s", str(e))
            return redirect('issue-backend')
        
    if request.method == 'POST' and 'cash' in request.POST:
        try:
            invoice_update = qs.stripe_cash_payment(invoice.invoice_id)
            invoice.fufiled = True
            invoice.paid = bal_due
            invoice.status = invoice_update.status
            invoice.save()
            
            return redirect('billing-details', id=invoice.id)
            
        except Exception as e:
            logging.error("Stripe invoice send operation failed: %s", str(e))
            return redirect('issue-backend')
    
    return render(request, 'billing/billing-details.html', {
        'invoice':invoice,
        'line_items':line_items,
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
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        hex_key = form.cleaned_data.get('hexkey')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        contact_method = form.cleaned_data.get('contact_method')
        address_1 = form.cleaned_data.get('address_1')
        address_2 = form.cleaned_data.get('address_2')
        city = form.cleaned_data.get('city')
        state = form.cleaned_data.get('state')
        zip_code = form.cleaned_data.get('zip_code')
        invite = Invite.objects.filter(hexkey=hex_key).first()
        if invite:

            user = form.save()
            user.groups.set('1')
            user.save()
            user_id = form.instance
            client = Client.objects.create(name=username, 
                                           email=email, 
                                           phone=phone, 
                                           contact_method=contact_method,
                                           address_1=address_1,
                                           address_2=address_2,
                                           city=city,
                                           state=state, 
                                           zip_code=zip_code,
                                           user_id=user_id
                                           )
            
            client.save()
            invite.used = True
            invite.save()
            return redirect('login')
        else:
            print('test 0')
            form.add_error('hexkey', 'Invalid hexkey. Please enter a valid key.')
            return self.form_invalid(form)

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
    dataQ.json_chart_data()

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
    
def notebook(request):
    
    project_list = Project.objects.all()
    client_list = Client.objects.all()
    image_list = Image.objects.all()
    print_list = Print.objects.all()
    
    return render(request, 'management/notebook.html', {
        'image_list': image_list,
        'print_list': print_list,
        'project_list': project_list,
        'client_list': client_list
    })
    
    
class PaymentsDetailView(DeleteView):
    model = Payments
    template_name = 'billing/payments/payment-details.html'