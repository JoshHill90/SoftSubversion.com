from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('management/main', views.o_main, name='o_main'),
    path('management/notebook', views.notebook, name='notebook'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit-profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    
    path('billing/', views.billing_panel, name='billing'),
    path('billing/<int:id>/details', views.billing_details, name='billing-details'),
    path('billing/create', BillCreateView.as_view(), name='billing-create'),
    path('billing/<int:pk>/edit', BillEditView.as_view(), name='billing-edit'),
    path('billing/<int:pk>/delete', BillDeleteView.as_view(), name='billing-delete'),
    
    path('<int:user_id>/change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'),
     name='change-password')
     

]