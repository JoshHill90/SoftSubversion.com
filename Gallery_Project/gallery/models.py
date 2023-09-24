from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import secrets
import random
import datetime

def hex_gen_small():
    fronter = 'SSP'
    random_num = random.randint(0, 99)
    random_hex = secrets.token_hex(4)
    print(random_hex)
    return fronter + str(random_hex) + str(random_num)

def date_stamp():
    date_and_time = datetime.datetime.now()
    dates = date_and_time.date()
    times = date_and_time.strftime("%I:%M:%S %p")
    date = str(dates)
    time = str(times)
    print(date)
    return date



DISPLAY_PEACE = [    
    ('none', 'none'),
    ('home1', 'home1'),
    ('home2', 'home2'),
    ('home3', 'home3'),
    ('home4', 'home4'),
    ('IOTM', 'IOTM'),
    ('gallery1', 'gallery1'),
    ('gallery2', 'gallery2'),
    ('gallery3', 'gallery3'),
    ('gallery4', 'gallery4'),
    ('subgal1', 'subgal1'),
    ('subgal2', 'subgal2'),
    ('subgal3', 'subgal3'),
    ('subgal4', 'subgal4'),
    ('project', 'project'),
    ('client', 'client',)]

ASPECT_RATIO = [    
    ('portrait', 'portrait'),
    ('landscape', 'landscape'),
]
    

class Project(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='Pending Deposit')
    client_id = models.ForeignKey('clients.Client', null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("project-details", args=(self.id,))
    
    
class Image(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    display = models.CharField(max_length=20, choices=DISPLAY_PEACE, default='portrait')
    aspect = models.CharField(max_length=20, choices=ASPECT_RATIO, default='none')
    client_id = models.ForeignKey('clients.Client', null=True, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    image_link = models.URLField(blank=True, default=' ')
    cloudflare_id = models.CharField(max_length=255, blank=True)
    silk_id = models.CharField(max_length=50, default='CB01')

    def __str__(self):
        return str(self.client_id.name + ' | ' + self.title)

    def get_absolute_url(self):
        return reverse("image-details", args=(self.id,))
    

class Print(models.Model):
    title = models.CharField(max_length=255)
    cost = models.FloatField(default=0.00)
    details = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    display = models.CharField(max_length=20, choices=DISPLAY_PEACE, default='none')
    aspect = models.CharField(max_length=20, choices=ASPECT_RATIO, default='none')
    image_link = models.URLField(blank=True, default=' ')
    cloudflare_id = models.CharField(max_length=255, blank=True)
    silk_id = models.CharField(max_length=50, default='CB01')
    

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("print-details", args=(self.id,))
    
class ProjectEvents(models.Model):
    title = models.CharField(max_length=255)
    payment_id = models.ForeignKey('management.Payments', on_delete=models.CASCADE, blank=True, null=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField(default=date_stamp())
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    event_type = models.CharField(max_length=50, blank=True)
    details = models.CharField(max_length=500, blank=True)

    
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("project-event", args=(self.id,))