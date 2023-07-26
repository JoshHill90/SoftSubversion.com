from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('about/', views.about_page, name='about'),
    path('social/', views.social_page, name='social'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success', ContactSuccess.as_view(), name='contact-success'),      
] 