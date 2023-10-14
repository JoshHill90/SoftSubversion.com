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
    
    path('invoice/', views.billing_panel, name='billing'),
    path('invoice/<int:id>/details', views.billing_details, name='billing-details'),
    path('invoice/create', BillCreateView.as_view(), name='billing-create'),
    path('invoice/<int:pk>/edit', BillEditView.as_view(), name='billing-edit'),
    path('invoice/<int:pk>/delete', BillDeleteView.as_view(), name='billing-delete'),
    
    path('invoice/line_item/<int:pk>/details', PaymentsDetailView.as_view(), name='payment-details'),
    
    path('<int:user_id>/change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'),
     name='change-password')
     

]