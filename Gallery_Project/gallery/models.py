from django.db import models
from django.urls import reverse
from Gallery_Project.clients.models import Client
from Gallery_Project.management.models import Coupon, Billing, Crew


    
class Project(models.Model):
    name = models.CharField(max_length=255)
    client_id = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    billing_id = models.ForeignKey(Billing, null=True, on_delete=models.CASCADE)
    cost = models.FloatField(default=0.00)
    status = models.BooleanField(default=False)
    crew_id = models.ForeignKey(Crew, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.client_id.name + ' | ' + self.name)

    def get_absolute_url(self):
        return reverse("project-details", args=(str(self.id)))
    
    
class Image(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    client_id = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    image_link = models.URLField(blank=True, default=' ')
    cloudflare_id = models.CharField(max_length=255, blank=True)
    silk_id = models.CharField(max_length=50, default='CB01')

    def __str__(self):
        return str(self.client_id.name + ' | ' + self.title)

    def get_absolute_url(self):
        return reverse("image-details", args=(str(self.id)))
    

class Print(models.Model):
    title = models.CharField(max_length=255)
    cost = models.FloatField(default=0.00)
    details = models.TextField(blank=True, null=True)
    image_link = models.URLField(blank=True, default=' ')
    cloudflare_id = models.CharField(max_length=255, blank=True)
    silk_id = models.CharField(max_length=50, default='CB01')
    

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("print-details", args=(str(self.id)))