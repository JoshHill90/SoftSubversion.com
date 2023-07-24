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

def IndexView(request):
    return render(request, template_name='index.html')

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

        return redirect('contact-success')