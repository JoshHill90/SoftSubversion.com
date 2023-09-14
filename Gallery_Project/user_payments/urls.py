from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('agreement', views.agreement, name='agreement'),
	#path('success', views.models, name='success'),
	#path('failed', views.models, name='failed'),
	#path('stripe_webhook', views.models, name='stripe_webhook'),
]