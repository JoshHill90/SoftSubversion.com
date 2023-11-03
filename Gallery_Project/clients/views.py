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
import stripe
from pathlib import Path
import os
from dotenv import load_dotenv
from Gallery_Project.env.app_Logic.json_utils import DataSetUpdate
from log_app.logging_config import logging
from Gallery_Project.env.app_Logic.MailerDJ import AutoReply
from Gallery_Project.env.app_Logic.stripe.quick_stripe import QuickStripe, DateFunction, Hexer

qs = QuickStripe()
df = DateFunction()
hexer = Hexer()
smtp_request = AutoReply

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)
stripe.api_key = os.getenv("STRIPE_KEY")

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
        hex_key = hexer.hex_gen()
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
    success_url = 'client.html'

def request_approval(request, id):
    try:
        client_request = get_object_or_404(ProjectRequest, id=id)
        user_info = User.objects.get(username=client_request.user_id)
        client_info = Client.objects.get(user_id__username=user_info.username)
        comments = RequestReply.objects.filter(project_request_id=client_request)
        new_template = None

        # Form validation and approval workflow
        if request.method == 'POST':
            terms_form = ProjectTermsForm(data=request.POST)
        
            if terms_form.is_valid():
                
                #----------------------------------------------------------------#
                # structures client and project infromation for addtional methods
                #----------------------------------------------------------------#
                
                # Process cleaned data from terms form
                terms_data = terms_form.cleaned_data
                project_amount = terms_data.get('project_cost')
                deposit_amount = terms_data.get('deposit')
                services = terms_data.get('services')

                # update the project request
                client_request.status = 'Approved'
                client_request.save()
                
                # Extracts users billing information
                full_name, full_address, phone, email_address = qs.stripe_user_extractor(user_info, client_info)
                
                        # check if customer exist in stripe db
                if not client_info.strip_id:
                    stripe_id = qs.stripe_user_creation(
                        client_info, 
                        full_name, 
                        email_address, 
                        full_address, 
                        phone
                    )
                    
                    # Saving new strip customer id
                    client_info.strip_id = stripe_id
                    client_info.save()
                else:
                    stripe_id = client_info.strip_id

                #----------------------------------------------------------------#
                # creates the corresponding prject, billing and project-terms
                #----------------------------------------------------------------#
                
                # creates project
                new_project_model = Project.objects.create(
                    name=client_request.name,
                    user_id=user_info,
                    client_id=client_info
                )
                
                # creates the billing corresponding stripe invoice for the project
                request_date_distance = df.date_distance(client_request.date)
                project_date_distance = request_date_distance + 30
                strip_project_invoice = qs.create_stripe_invoice(stripe_id, project_date_distance, services)

                # creates new billing account for client 
                new_billing_model = Billing.objects.create(
                    project_id=new_project_model,
                    invoice_id=strip_project_invoice.id,
                    status = strip_project_invoice.status,
                    details=services,
                    due_date = df.number_to_days(project_date_distance),
                    payment_type='Project Invoice'
                )
                
                # creates new Project Terms  
                new_template = terms_form.save(commit=False)
                
                new_template.user_id = user_info
                new_template.project_request_id = client_request
                new_template.scope = client_request.scope
                new_template.project_docs = f"{user_info}/{client_request.name}"
                new_template.project_id = new_project_model
                
                new_template.save()
                #----------------------------------------------------------------#
                # checks for deposit and project cost and process if they exist
                #----------------------------------------------------------------#
                converted_to_cents = lambda dollar_amount: int(
                    str(
                        '{:.2f}'.format(
                            float(dollar_amount))).replace('.','')
                )
                if deposit_amount > 0:
                    deposit_date = df.deposit_distance(client_request.date)
                    deposit_details = f'Deposit for photography project:{new_project_model.name}'
                    deposit = converted_to_cents(deposit_amount)
                    deposit_invoice = qs.create_stripe_invoice(stripe_id, deposit_date, deposit_details)

                    
                    deposit_lineitem = qs.create_stripe_line_item(deposit, 'Deposit Cost', deposit_invoice, stripe_id)
                    payment_link, deposit_invoice_update = qs.send_stripe_invoice(deposit_invoice.id)
                    deposit_billing = Billing.objects.create(
                        project_id=new_project_model,
                        invoice_id=deposit_invoice.id,
                        details=deposit_details,
                        billed=deposit_amount,
                        status=deposit_invoice_update.status,
                        due_date = df.number_to_days(deposit_date),
                        payment_link=payment_link,
                        payment_type='Deposit'
                    )
                    
                    Payments.objects.create(
                        billing_id=deposit_billing,
                        amount=deposit_amount,
                        receipt='Deposit Cost',
                        time_stamp=df.date_now(),
                        item_id=deposit_lineitem.id,
                    )
                    
                    ProjectEvents.objects.create(
                        title='Deposit Reminder',
                        project_id=new_project_model,
                        billing_id=new_billing_model,
                        date=new_billing_model.due_date,
                        start=df.payment_time(),
                        end=df.payment_time(),
                        event_type='Payment Reminder',
                        details=f'Event for deposit reminder for project{new_project_model}'
                    )
    
                    qs.send_invoice_email(user_info, new_project_model, deposit_billing)

                if project_amount > 0:
                    project_cost = converted_to_cents(project_amount)
                    project_lineitem = qs.create_stripe_line_item(project_cost, 'Project Cost', strip_project_invoice, stripe_id)
                    Payments.objects.create(
                        billing_id=new_billing_model,
                        amount=project_amount,
                        receipt='Project Cost',
                        time_stamp=df.date_now(),
                        item_id=project_lineitem.id,
                    )
                    
                    new_billing_model.billed = project_amount
                    new_billing_model.save()
                    
            return redirect('project-details', new_project_model.id)

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
        
    except Exception as e:
        logging.error("Stripe customer create method failed: %s", str(e))
        return redirect('issue-backend')

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
        randnum = hexer.hex_gen_small()
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
            return redirect('client-comment-success')

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
    
class ClientCommentSuccessView(TemplateView):
    template_name = 'client_portal/success/comment-success.html'
    
class CommentSuccessView(TemplateView):
    template_name = 'client/success/comment_success.html'
    
#-------------------------------------------------------------------------------------------------------#
# failed static views 
#-------------------------------------------------------------------------------------------------------#
    
class FailedInvite(TemplateView):
    template_name = 'client/success/failed-invite.html'