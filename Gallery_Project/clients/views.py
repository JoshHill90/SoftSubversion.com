from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from pathlib import Path
from .models import Client, Invite, ProjectRequest, RequestReply, ProjectTerms
from .forms import ClientForm, InviteForm, ProjectRequestForm, RequestReplyComment, ProjectTermsForm
from gallery.models import Image, Project, ProjectEvents
from gallery.forms import ProjectEventForms
from management.models import Payments, Billing
from django.shortcuts import render, redirect, get_object_or_404
import secrets
import stripe
from Gallery_Project.env.app_Logic.MailerDJ import AutoReply
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from Gallery_Project.env.app_Logic.json_utils import DataSetUpdate

        

# -------------------------------------------------------------------------------------------------------------#
# Date and time configeration
# -------------------------------------------------------------------------------------------------------------#

def in_30_days():
    date_and_time = datetime.now()
    dates = date_and_time.date()
    date_30 = dates + timedelta(days=30)
    return date_30

def in_60_days():
    date_and_time = datetime.now()
    dates = date_and_time.date()
    date_60 = dates + timedelta(days=60)
    return date_60

def in_90_days():
    date_and_time = datetime.now()
    dates = date_and_time.date()
    date_90 = dates + timedelta(days=90)
    return date_90

def in_182_days():
    date_and_time = datetime.now()
    dates = date_and_time.date()
    date_90 = dates + timedelta(days=90)
    return date_90

def date_now():
    date_and_time = datetime.now()
    dates = date_and_time.date()
    return dates

def date_setter(desired_date):
    due_on = ''
    desired_date_str = str(desired_date)
    
    requested_date = datetime.strptime(desired_date_str, "%Y-%m-%d").date()
    date_and_time = datetime.now()
    dates = date_and_time.date()
    
    if (requested_date - dates).days <= 30:
        due_on = str(in_30_days())
        
    elif (requested_date - dates).days <= 60:
        due_on = str(in_60_days())
        
    elif (requested_date - dates).days <= 90:
        due_on = str(in_90_days())
        
    else:
        due_on = str(in_182_days())
        
    return due_on 

def date_distance(desired_date):
    due_in = ''
    desired_date_str = str(desired_date)
    
    requested_date = datetime.strptime(desired_date_str, "%Y-%m-%d").date()
    date_and_time = datetime.now()
    dates = date_and_time.date()
    
    if (requested_date - dates).days <= 30:
        due_in = 5
        
    elif (requested_date - dates).days <= 60:
        due_in = 30
        
    elif (requested_date - dates).days <= 90:
        due_in = 60
        
    else:
        due_in = 182
        
    return due_in 

def deposit_distance(desired_date):
    desired_date_str = str(desired_date)

    
    requested_date = datetime.strptime(desired_date_str, "%Y-%m-%d").date()
    date_and_time = datetime.now()
    dates = date_and_time.date()
    
    if (requested_date - dates).days <= 30:
        due_in = 5
        
    else:
        due_in = 30

        
    return due_in 

#-------------------------------------------------------------------------------------------------------#
# smtp global
#-------------------------------------------------------------------------------------------------------#

smtp_request = AutoReply()

#-------------------------------------------------------------------------------------------------------#
# ownder client views 
#-------------------------------------------------------------------------------------------------------#

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)
stripe.api_key = os.getenv("STRIPE_KEY")

#-------------------------------------------------------------------------------------------------------#
# hex_gen
#-------------------------------------------------------------------------------------------------------#

def hex_gen():
    random_hex = secrets.token_hex(16)
    return str(random_hex)

def hex_gen_small():
    random_hex = secrets.token_hex(4)
    return str(random_hex)

#-------------------------------------------------------------------------------------------------------#
# ownder client views 
#-------------------------------------------------------------------------------------------------------#

def client_main(request):
    client_list = Client.objects.exclude(Q(name='Soft Subversion'))
    client_images = Image.objects.exclude(Q(client_id__name="Soft Subversion"))
    project_list = Project.objects.exclude(Q(user_id__username="Soft Subversion"))
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
    client_info = Client.objects.get(id=client_id)
    user_info = User.objects.get(username=client_info.name)
    client_project = Project.objects.filter(client_id=client_info)
    image_list = Image.objects.filter(client_id=client_info)
    return render(request, 'client/client-details.html', {
		'client_info': client_info,
        'user_info': user_info,
        'client_project': client_project,
        'image_list':image_list
        
    })

class ClientIntake(CreateView):
    form_class = InviteForm
    model = Invite
    template_name = 'client/client-invite.html'
    
    def form_valid(self, form):
        self.object = form.save()
        email = form.cleaned_data.get('email',)
        name = form.cleaned_data.get('email',)
        hex_key = hex_gen()
        add_feild = self.object
        add_feild.hexkey = hex_key
        add_feild.save()
        response_back = smtp_request.send_invite(email, name, hex_key)
        if response_back == 'sent':
            dataQ = DataSetUpdate()
            dataQ.json_user_list_check()
            return redirect('invite-success')
        else:
            return redirect('invite-failed')
        
def clientRequestDetails(request, slug):
    project_request = get_object_or_404(ProjectRequest, slug=slug)
    print(project_request.id)
    comments = RequestReply.objects.filter(project_request_id=project_request.id)
    new_comments = None
    if request.method == 'POST':
        comment_form = RequestReplyComment(data=request.POST)
        if comment_form.is_valid():
            user_info = request.user
            new_comment = comment_form.save(commit=False)
            new_comment.user_id = user_info
            new_comment.project_request_id = project_request
            new_comment.save()
            comment = comment_form.cleaned_data.get('comment')
            clinet_email = user_info.email
            smtp_request.owner_post_comment(clinet_email, user_info, comment, project_request, slug)
            return redirect('comment-success')

    else:
        comment_form = RequestReplyComment()
    
    return render(request, 'client/request-details.html', {
		'projectrequest': project_request,
        'comment_form': comment_form,
        'new_comments' : new_comments,
        'comments': comments, 
  })
    

def client_request(request):
    client_request = ProjectRequest.objects.all()
    request_comments = RequestReply.objects.all()
    request_comments = RequestReply.objects.all()
    project_terms = ProjectTermsForm
    client_request
    return render(request, 'client/client-requests.html', {
		'client_request': client_request,
        'request_comments' : request_comments,
        'project_terms': project_terms
  })

class CleintDeleteView(DeleteView):
    model = Client
    template_name = 'client/client-delete.html'

def request_approval(request, id):
    
    client_request = get_object_or_404(ProjectRequest, id=id)
    user_info = User.objects.get(username=client_request.user_id)
    client_info = Client.objects.get(user_id__username=user_info.username)
    comments = RequestReply.objects.filter(project_request_id=client_request)
    new_template = None
    
    # Form validation and approval workflow
    if request.method == 'POST':
        terms_form = ProjectTermsForm(data=request.POST)
        if terms_form.is_valid():
            
            # creates project
            new_project = Project.objects.create(
                name=client_request.name,
                user_id=user_info,
                client_id=client_info
            )
            
            new_template = terms_form.save(commit=False)
            if len(str(client_request.slug)) > 16:
            
                new_template.slug = 'terms' + str(client_request.slug[0:17]) + hex_gen_small()
            else:
                new_template.slug = 'terms' + str(client_request.slug) + hex_gen_small()
            
            new_template.user_id = user_info
            new_template.project_request_id = client_request
            new_template.scope = client_request.scope
            
            new_template.project_docs = f"{user_info}/{client_request.name}"
            new_template.project_id = new_project
           

            # Process cleaned data
            terms_data = terms_form.cleaned_data
            project_amount = terms_data.get('project_cost')
            services = terms_data.get('services')
            deposit_amount = terms_data.get('deposit')
            slug = terms_data.get('slug')

            # update the project request
            client_request.status = 'Approved'
            client_request.save()

            # Extract client info
            firstname = user_info.first_name
            lastname = user_info.last_name
            address1 = client_info.address_1
            address2 = client_info.address_2
            phone = client_info.phone
            city = client_info.city
            state = client_info.state
            zipcode = client_info.zip_code
            full_name = f"{firstname} {lastname}"

            # lmabda function to convert from dollars to cents 
            format_amount = lambda dollar_amount: int(
                str(
                    '{:.2f}'.format(
                        float(dollar_amount))).replace('.','')
                )
            deposit = format_amount(deposit_amount)
            project_cost = format_amount(project_amount)
    
            #deposit_amount = float(deposit_amount)
            #flt_deposit = '{:.2f}'.format(deposit_amount)
            #str_deposit = str(flt_deposit) 
            #deposit = int(str_deposit.replace('.', ''))
            
            full_address = {'line1':address1, 'line2':address2, 'city':city, 'state': state, 'postal_code':zipcode, 'country':'US'  }
            email_address = user_info.email

            # check if customer exist in stripe db
            if not client_info.strip_id:
                strip_customer = stripe.Customer.create(
                                                        name=full_name,
                                                        email=email_address,
                                                        address=full_address,
                                                        phone=phone
                                                        )
                # Saving new strip customer id
                client_info.strip_id = strip_customer.id
                client_info.save()
                
                stripe_id = strip_customer.id
                stripe_prefix = strip_customer.invoice_prefix
                print(stripe_id)
                
            # for existing strip cust id   
            else:
                strip_customer = stripe.Customer.retrieve(
                    id=client_info.strip_id
                )
                stripe_id = client_info.strip_id
                stripe_prefix = strip_customer.invoice_prefix
                
                
            # create invoice for deposit
            stripe_invoice_deposit = stripe.Invoice.create(
                customer=stripe_id,
                collection_method='send_invoice',
                days_until_due=deposit_distance(client_request.date),
                description=services,
            )
            
            # creates line item charge for deposit
            deposit_line_item = stripe.InvoiceItem.create(
                    amount=deposit,
                    currency='usd', 
                    description= 'Deposit',
                    discountable= False,
                    invoice=stripe_invoice_deposit.id,
                    customer=stripe_id
            )
            
            
            # create invoice for the project
            stripe_invoice_project = stripe.Invoice.create(
                customer=stripe_id,
                collection_method='send_invoice',
                days_until_due=date_distance(client_request.date),
                description=services,
            )
            
            # creates line item charge for  the project
            project_cost_line_item = stripe.InvoiceItem.create(
                    amount=project_cost,
                    currency='usd', 
                    description= 'Project Cost',
                    discountable= False,
                    invoice=stripe_invoice_project.id,
                    customer=stripe_id
            )
            
            # send the invoice and pulls the payment link and the new invoice data 
            deposit_invoice_out = stripe.Invoice.send_invoice(invoice=stripe_invoice_deposit.id)
            deposit_payment_link = deposit_invoice_out.hosted_invoice_url
            deposit_invoice_update = stripe.Invoice.retrieve(id=stripe_invoice_deposit.id)
            
            project_invoice_out = stripe.Invoice.send_invoice(invoice=stripe_invoice_project.id)
            project_payment_link = project_invoice_out.hosted_invoice_url
            project_invoice_update = stripe.Invoice.retrieve(id=stripe_invoice_project.id)
            
            # creates new billing account for client 
            new_billing = Billing.objects.create(
                invoice=stripe_prefix,
                billed=project_amount + deposit_amount,
                project_id=new_project,
                due_date=date_setter(client_request.date)
            )
            
            # creates new payment/invoice for deposit
            deposit_payment = Payments.objects.create(
                billing_id=new_billing,
                amount=deposit_amount,
                receipt='Deposit Cost',
                status=deposit_invoice_update.status,
                time_stamp=date_now(),
                invoice_id=deposit_invoice_update.id,
                payment_link=deposit_payment_link,
                due_date=in_30_days()
            )
            
            # creates new payment/invoice for project cost
            project_payment = Payments.objects.create(
                billing_id=new_billing,
                amount=project_amount,
                receipt="Project Cost",
                status=project_invoice_update.status,
                time_stamp=date_now(),
                invoice_id=project_invoice_update.id,
                payment_link=project_payment_link,
                due_date=date_setter(client_request.date)
            )
            
            ProjectEvents.objects.create(
                title='Deposit Reminder',
                payment_id=deposit_payment,
                project_id=new_project,
                date=deposit_payment.due_date,
                start=datetime.strptime("5:00 pm", "%I:%M %p").time(),
                end=datetime.strptime("5:00 pm", "%I:%M %p").time(),
                event_type='Deposit Reminder',
                details='Event for deposit reminder'
            )
            
            
            ProjectEvents.objects.create(
                title='Project Payment',
                payment_id=project_payment,
                project_id=new_project,
                date=project_payment.due_date,
                start=datetime.strptime("5:00 pm", "%I:%M %p").time(),
                end=datetime.strptime("5:00 pm", "%I:%M %p").time(),
                event_type='Project Payment',
                details='Event for project payment'
            )
            project_link = f"https://SoftSubversion.com/client-portal/project-binder/{new_project.id}/details"
            invoice_link = f"https://SoftSubversion.com/client-portal/billing/invoice/{deposit_payment.id}/"
            smtp_request.new_project_and_invoice(user_info.email,
                                                 user_info.first_name,
                                                 deposit_payment.payment_link,
                                                 project_link,
                                                 invoice_link
                                                 )
            #saving form at the end after everything is done.
            new_template.save()
            
            return redirect('project-details', new_project.id)

    else:
        terms_form = ProjectTermsForm()
    
    return render(request, 'client/request/request-approval.html', {
		'client_request': client_request,
        'user_info': user_info,
        'comments': comments,
        'client_info': client_info,
        'terms_form': terms_form,
        'new_template': new_template
  })
# defualt consultation createion page, for use after the project is approved 
# lets not talk about why i chose to indlue it here. 
def request_event(request, payment_id):
    cal_form = ProjectEventForms.objects.all()
    new_event = None
    
   
    if request.method == 'POST':
        event_form = ProjectEventForms(data=request.POST)
        if event_form.is_valid():
            
            return render(request, 'client/request/request_consultation.html')
    
    return render(request,'client/request/request_consultation.html', {
        'form':cal_form
    } )

#-------------------------------------------------------------------------------------------------------#
# client project views 
#-------------------------------------------------------------------------------------------------------#

def project_binder(request, id):
    users_id = id
    client = Client.objects.get(user_id=users_id)
    client_id = client.id
    client_images = Image.objects.filter(Q(client_id=client_id))
    project_list = Project.objects.filter(Q(user_id__id=users_id))
    project_request_info = ProjectRequest.objects.filter(Q(user_id__id=users_id))
    request_comments = RequestReply.objects.filter(Q(user_id__id=users_id))
                	
    return render(request, 'client_portal/project-binder.html', {
		'client_info': client,
		'client_images':client_images,
		'project_list': project_list,
        'project_request': project_request_info,
        'comments': request_comments
	})
    
class ProjectRquestCreate(CreateView):
    form_class = ProjectRequestForm
    model = ProjectRequest
    
    template_name = 'client_portal/projects/project-request.html'
    def form_valid(self, form):

        
        user_info = self.request.user
        user_id = user_info.id
        client = user_info.username
        user_info.user_id = user_id
        
        project_name = form.cleaned_data.get('name')
        date_selected = form.cleaned_data.get('date')
        scope = form.cleaned_data.get('scope')
        details = form.cleaned_data.get('details')
        location_type = form.cleaned_data.get('location')


        
        project_request = form.save(commit=False)
        
        id_str = str(user_id)
        project_name_str = str(project_name)
        clean_name = project_name_str.replace(' ', '-')
        randnum = hex_gen_small()
        pj_id = str(randnum)

        slug_str = str(id_str + '-' + pj_id + '-' + 'prj')
        
        project_request.user_id_id = user_id 
        project_request.slug = slug_str
        project_request.save()
        
        smtp_request.project_request_notice(project_name, date_selected, scope, details, location_type, user_id, client)
        return redirect('request-status', slug_str)
    
def request_status(request, slug):
    project_request = get_object_or_404(ProjectRequest, slug=slug)
    print(project_request.id)
    comments = RequestReply.objects.filter(project_request_id=project_request.id)
    new_comments = None
    if request.method == 'POST':
        comment_form = RequestReplyComment(data=request.POST)
        if comment_form.is_valid():
            user_info = request.user
            new_comment = comment_form.save(commit=False)
            new_comment.user_id = user_info
            new_comment.project_request_id = project_request
            new_comment.save()
            comment = comment_form.cleaned_data.get('comment')
            return render(request, 'client/comment_success.html', {
                'slug': slug,
            })

    else:
        comment_form = RequestReplyComment()
    
    return render(request, 'client_portal/projects/request-status.html', {
		'projectrequest': project_request,
        'comment_form': comment_form,
        'new_comments' : new_comments,
        'comments': comments, 
  })
    
#-------------------------------------------------------------------------------------------------------#
# success static views
#-------------------------------------------------------------------------------------------------------#   
    
class SuccessInvite(TemplateView):
    template_name = 'client/success/success-invite.html'
    
class CommentSuccessView(TemplateView):
    template_name = 'client/success/comment_success.html'
    
#-------------------------------------------------------------------------------------------------------#
# failed static views 
#-------------------------------------------------------------------------------------------------------#
    
class FailedInvite(TemplateView):
    template_name = 'client/success/failed-invite.html'