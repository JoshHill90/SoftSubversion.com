from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .views import *
from . import views

urlpatterns = [
    path('', views.client_main, name='client'),
    path('<int:client_id>/details', views.client_details, name='client-details'),
    path('intake', ClientIntake.as_view(), name='client-intake'),
    path('<int:id>/binder', views.project_binder, name='project-binder'),
]