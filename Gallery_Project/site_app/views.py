from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Contact
from .forms import ContactForm
from Gallery_Project.env.app_Logic.MailerDJ import AutoReply

EMAIL = AutoReply()

def index_page(request):

    return render(request, 'index.html')

def about_page(request):
    return render(request, 'about.html')

def social_page(request):
    return render(request, 'social.html')

class ContactView(FormView):
    model = Contact
    template_name = 'contact.html'
    form_class = ContactForm
    def form_valid(self, form):
        self.object = form.save()
        name = self.object.name
        email = self.object.email
        subject = self.object.subject
        body = self.object.body

        EMAIL.contact_request(email, name)
        EMAIL.contact_alart(email, name, subject, body)

        return render(self.request, 'success/contact-success.html', {
            'name': name, 
            'email': email,
            'subject': subject,
        })
    
class ContactSuccess(TemplateView):
    template_name = 'success/contact-success.html'