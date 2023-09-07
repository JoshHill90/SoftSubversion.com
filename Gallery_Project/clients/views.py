from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from pathlib import Path
from .models import Client, Invite, ProjectRequest, RequestReply
from .forms import ClientForm, InviteForm, ProjectRequestForm, RequestReplyComment
from gallery.models import Image, Project
from management.models import Payments, Billing
from django.shortcuts import render, redirect, get_object_or_404
import secrets
from Gallery_Project.env.app_Logic.MailerDJ import AutoReply

smtp_request = AutoReply()

def hex_gen():
    random_hex = secrets.token_hex(16)
    print(random_hex)
    return str(random_hex)

def hex_gen_small():
    random_hex = secrets.token_hex(2)
    print(random_hex)
    return str(random_hex)

#-------------------------------------------------------------------------------------------------------#
# ownder client views 
#-------------------------------------------------------------------------------------------------------#

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
            return render(request, 'client/comment_success.html', {
                'slug': slug,
            })

    else:
        comment_form = RequestReplyComment()
    
    return render(request, 'client/request-details.html', {
		'projectrequest': project_request,
        'comment_form': comment_form,
        'new_comments' : new_comments,
        'comments': comments, 
  })
    

def client_request(request):
    client_request_info = ProjectRequest.objects.all()
    request_comments = RequestReply.objects.all()
    
    return render(request, 'client/client-requests.html', {
		'client_request': client_request_info,
        'request_comments' : request_comments
  })

def request_approval(request, id):
    client_request_info = ProjectRequest.objects.all()
    request_comments = RequestReply.objects.all()
    
    return render(request, 'client/request/request-approval.html', {
		'client_request': client_request_info,
        'request_comments' : request_comments
  })
        
        
class CommentSuccessView(TemplateView):
    template_name = 'client/comment_success.html'
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

        slug_str = str('USID-' + id_str + '-unq-' + pj_id + '-PJN-' + clean_name)
        
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