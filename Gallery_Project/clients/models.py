from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

    
class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Prefered Name')
    phone = models.CharField(max_length=10, verbose_name='Contact Phone Number')
    email = models.EmailField(max_length=100, verbose_name='Email Address' )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(str(self.id)))