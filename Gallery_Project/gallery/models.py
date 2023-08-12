from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

DISPLAY_PEACE = [    
    ('none', 'none'),
    ('home1', 'home1'),
    ('home2', 'home2'),
    ('home3', 'home3'),
    ('home4', 'home4'),
    ('gallery1', 'gallery1'),
    ('gallery2', 'gallery2'),
    ('gallery3', 'gallery3'),
    ('gallery4', 'gallery4'),
    ('project', 'project'),
    ('client', 'client',)]
    

class Project(models.Model):
    name = models.CharField(max_length=255)
    cost = models.FloatField(default=0.00)
    status = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user_id.username + ' | ' + self.name)

    def get_absolute_url(self):
        return reverse("project-details", args=(str(self.id)))
    
    
class Image(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    display = models.CharField(max_length=20, choices=DISPLAY_PEACE, default='none')
    client_id = models.ForeignKey('clients.Client', null=True, on_delete=models.CASCADE)
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
    status = models.BooleanField(default=False)
    display = models.CharField(max_length=20, choices=DISPLAY_PEACE, default='none')
    image_link = models.URLField(blank=True, default=' ')
    cloudflare_id = models.CharField(max_length=255, blank=True)
    silk_id = models.CharField(max_length=50, default='CB01')
    

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("print-details", args=(str(self.id)))