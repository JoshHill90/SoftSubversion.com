from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('management/main', views.o_main, name='o_main'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit-profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('<int:user_id>/change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'),
     name='change-password')
     

]