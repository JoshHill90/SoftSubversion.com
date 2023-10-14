from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .views import *
from . import views

urlpatterns = [
    path('', views.client_main, name='client'),
    path('<int:client_id>/details', views.client_details, name='client-details'),
    path('intake', ClientIntake.as_view(), name='client-intake'),
    path('client/delete/<int:pk>', CleintDeleteView.as_view(), name='client-delete'),
    path('requests/', views.client_request, name='client-request'),
    path('requests/<slug:slug>', views.clientRequestDetails, name='request-details'),
    
    path('<int:id>/binder', views.project_binder, name='project-binder'),
    path('binder/project-request', ProjectRquestCreate.as_view(), name='project-request'),
    path('binder/request_status/<slug:slug>',views.request_status, name='request-status'),

    path('client/request/approval/<int:id>', views.request_approval, name='approval'),

    path('client/comment_success', CommentSuccessView.as_view(), name='comment-success'),
    path('client/invite/success', SuccessInvite.as_view(), name='invite-success'),
    
    path('binder/comment-success', ClientCommentSuccessView.as_view(), name='client-comment-success'),
    
    path('client/invite/failed', SuccessInvite.as_view(), name='invite-failed'),
    
]