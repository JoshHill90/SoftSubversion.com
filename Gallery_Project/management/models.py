from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

    
class Crew(models.Model):
    name = models.CharField(max_length=255, verbose_name='Prefered Name')
    phone = models.CharField(max_length=10, verbose_name='Contact Phone Number')
    email = models.EmailField(max_length=100, verbose_name='Contact Phone Number')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(str(self.id)))
    
class Memeber(models.Model):
    name = models.CharField(max_length=255, verbose_name='Prefered Name')
    phone = models.CharField(max_length=10, verbose_name='Contact Phone Number')
    email = models.EmailField(max_length=100, verbose_name='Contact Phone Number')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(str(self.id)))
    


    
class Coupon(models.Model):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("cupon-details", kwargs={"pk": self.pk})

class Billing(models.Model):

    client_id = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    billed = models.FloatField(default=0.00)
    paid = models.FloatField(default=0.00)
    crew_id = models.ForeignKey(Crew, on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)
    project_id = models.ForeignKey('gallery.Project', on_delete=models.CASCADE)
    cupon_id = models.ForeignKey(Coupon, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.id + ' | ' + self.client_id.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(str(self.id)))
    

    