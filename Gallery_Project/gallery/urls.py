from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('gallery/', views.gallery_hall, name='gallery'),
    path('gallery/models', views.model_gallery, name='model'),
    path('gallery/prints', views.prints_gallery, name='prints'),
    path('gallery/weddings', views.wedding_gallery, name='wedding'),
    path('gallery/family', views.family_gallery, name='family'),

    path('image/', ImageListView.as_view(), name='images'),
    path('image/<int:pk>/details', ImageDetailView.as_view(), name='image-details'),
    path('image/<int:pk>/edit', ImageEditView.as_view(), name='image-edit'),
    path('image/<int:pk>/delete', ImageDeleteView.as_view(), name='image-delete'),

    path('print/', PrintListView.as_view(), name='prints-all'),
    path('print/<int:pk>/details', PrintDetailView.as_view(), name='print-details'),
    path('print/<int:pk>/edit', PrintEditView.as_view(), name='print-edit'),
    path('print/<int:pk>/delete', PrintDeleteView.as_view(), name='print-delete'),

    path('project/', views.project_main, name='projects'),
    path('project/<int:pk>/details', views.project_owner_view, name='project-details'),
    path('project/create', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/edit', ProjectEditView.as_view(), name='project-edit'),
    path('project/<int:pk>/delete', ProjectDeleteView.as_view(), name='project-delete'),
    
    path('image/create/<str:clfr_id>', CreateImage.as_view(), name='image-create'),
    path('print/create/<str:clfr_id>', PrintCreateView.as_view(), name='print-create'),
    path('image/upload', upload_image, name='image-upload'),
    
    path('project/<int:pk>/event',ProjectEventsDetails.as_view() , name='project-event'),
    path('project/<int:pk>/event/edit',ProjectEventsEdit.as_view() , name='edit-event'),
    path('project/<int:pk>/event/delete',ProjectEventsDelete.as_view() , name='delete-event'),
    path('project/event/new', ProjectEventsCreate.as_view() , name='new-event'),
    path('project/events/<int:year>/<str:month>', views.clandar, name='project-calendar'),
    
    path('project/<int:id>/gallery',views.project_gallery , name='project-gallery'),
    
    path('project/<int:id>/notes',views.project_notes , name='project-notes'),
] 