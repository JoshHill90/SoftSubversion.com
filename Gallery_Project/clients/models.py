from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse



    
class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Prefered Name')
    phone = models.CharField(max_length=10, verbose_name='Contact Phone Number')
    email = models.EmailField(max_length=100, verbose_name='Email Address')
    contact_method = models.CharField(max_length=255, verbose_name=' - ')
    address_1 = models.CharField(max_length=255, verbose_name='Street Address/PO Box')
    address_2 = models.CharField(max_length=255, verbose_name='Apt/Suite')
    city = models.CharField(max_length=255, verbose_name='City')
    state = models.CharField(max_length=255, verbose_name='State')
    zip_code =models.CharField(max_length=255, verbose_name='Zipcode')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    crew_id = models.ForeignKey('management.Crew', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(str(self.id)))
    
class Invite(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    email = models.EmailField(max_length=100, verbose_name='Email Address' )
    hexkey = models.CharField(max_length=32)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client")