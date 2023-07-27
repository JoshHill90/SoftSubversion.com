from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('blog/', all_blogs, name='blogs'),
    path('blog/<int:pk>', views.blog_details, name='blog-details'),
    path('blog/<int:pk>/edit', BlogEditView.as_view(), name='blog-edit'),
    path('blog/<int:pk>/delete', BlogDeleteView.as_view(), name='blog-delete'),
    path('blog/create', BlogCreateView.as_view(), name='blog-create'),
]