from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
import stripe
from dotenv import load_dotenv
import os
from pathlib import Path
    
current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)    

email_host = os.getenv("EMAIL_HOSTING")

    

@login_required(login_url='login')
def agreement(request):
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					''
				}
			]
		)
			