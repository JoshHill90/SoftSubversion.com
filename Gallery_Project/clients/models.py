from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from Gallery_Project.gallery.models import Project

    
class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Prefered Name')
    phone = PhoneNumberField(max_length=10, verbose_name='Contact Phone Number', region='US')
    email = models.EmailField(max_length=100, verbose_name='Contact Phone Number' )
    project_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(str(self.id)))