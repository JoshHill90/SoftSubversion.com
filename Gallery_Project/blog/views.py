from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Blog
from .forms import BlogForm

class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog-create.html'

class BlogEditView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog-edit.html'

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog-delete.html'
    success_url = reverse_lazy('index')

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog-detail.html'
    success_url = reverse_lazy('index')

def all_blogs(request):
    blog_list = Blog.objects.all()
    title_query = request.GET.get('title')
    keyword_query = request.GET.get('keyword')
    orrder_query = request.GET.get('order')
    
    
    if not (keyword_query or title_query):
        blog_list = Blog.objects.all()
    elif keyword_query:
        blog_list = Blog.objects.filter(
            Q(title__icontains=keyword_query) | Q(article__icontains=keyword_query)
            )
    elif title_query:
        blog_list = Blog.objects.filter(title__icontains=title_query)
    elif keyword_query == None and title_query == None:
        blog_list = Blog.objects.all()
    
    if orrder_query == 'Oldest':
        blog_list = blog_list.order_by('time_stamp')
    else:
        blog_list = blog_list.order_by('-time_stamp')
    
    return render(request, 'blog/blogs.html', {
        'blog_list': blog_list
        }
    )