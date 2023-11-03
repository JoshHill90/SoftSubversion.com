from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
import datetime
import secrets

def hex_gen_small():
    random_hex = secrets.token_hex(2)
    print(random_hex)
    return str(random_hex)

date_and_time = datetime.datetime.now()
dates = date_and_time.date()
times = date_and_time.strftime("%I:%M:%S %p")
date_now = str(dates)

    
class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Prefered Name')
    strip_id = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=10, verbose_name='Contact Phone Number')
    email = models.EmailField(max_length=100, verbose_name='Email Address')
    address_1 = models.CharField(max_length=255, verbose_name='Street Address/PO Box')
    address_2 = models.CharField(max_length=255, verbose_name='Apt/Suite')
    city = models.CharField(max_length=255, verbose_name='City')
    state = models.CharField(max_length=255, verbose_name='State')
    zip_code =models.CharField(max_length=255, verbose_name='Zipcode')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(self.id))
    
class Invite(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    email = models.EmailField(max_length=100, verbose_name='Email Address' )
    hexkey = models.CharField(max_length=32)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("project-binder", args=(str(self.id)))
    

class ProjectRequest(models.Model):
    name = models.CharField(max_length=255, verbose_name='Project Name')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    date = models.CharField(max_length=10)
    scope = models.CharField(max_length=255, verbose_name='Project-Type/Scope')
    details = models.CharField(max_length=3000, verbose_name='Project Details')
    slug = models.SlugField(null=False, unique=True, max_length=32)
    location = models.CharField(max_length=255, verbose_name='Location type')
    status = models.CharField(max_length=25, default='pending')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        
        return reverse("request-status", kwargs={"slug": self.slug})
    
class RequestReply(models.Model):
    project_request_id = models.ForeignKey(ProjectRequest, on_delete=models.CASCADE, )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=3000)
    date_posted = models.DateField(auto_now=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.project_request_id) + ' | ' + str(self.user_id)

    def get_absolute_url(self):
        
        return reverse("request-status", kwargs={"slug": self.slug})
    
class ProjectTerms(models.Model):
    project_request_id = models.ForeignKey(ProjectRequest, on_delete=models.CASCADE, )
    project_id = models.ForeignKey('gallery.Project', on_delete=models.CASCADE, )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    scope = models.CharField(max_length=255)
    services = models.TextField(max_length=5000, blank=True)
    slug = models.SlugField(null=False, unique=True, default=hex_gen_small())
    project_cost = models.FloatField(default='600.00')
    deposit = models.FloatField(default='0.00')
    project_docs = models.CharField(max_length=255)

    def __str__(self):
        return str(self.project_request_id) + ' | ' + str(self.user_id)

    def get_absolute_url(self):
        
        return reverse("request-approval", kwargs={"slug": self.slug})