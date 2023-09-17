from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
import datetime

# -------------------------------------------------------------------------------------------------------------#
# Date and time configeration
# -------------------------------------------------------------------------------------------------------------#
def date_stamp():
    date_and_time = datetime.datetime.now()
    dates = date_and_time.date()
    times = date_and_time.strftime("%I:%M:%S %p")
    date = str(dates)
    time = str(times)
    print(date)
    return date



    
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
    
class Coupon(models.Model):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    percent = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("cupon-details", kwargs={"pk": self.pk})

class credit(models.Model):

    name = models.CharField(max_length=255)
    amount = models.FloatField(max_length=8, default=0.00)
    details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("cupon-details", kwargs={"pk": self.pk})

class Billing(models.Model):

    invoice = models.CharField(max_length=100)
    billed = models.FloatField(default=0.00)
    paid = models.FloatField(default=0.00)
    fufiled = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, default=date_stamp())
    open_date = models.DateField(auto_now=True)
    project_id = models.OneToOneField('gallery.Project', on_delete=models.CASCADE)
    cupon_id = models.ForeignKey(Coupon, null=True, on_delete=models.SET_NULL)
    credit_id = models.ForeignKey(credit, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        ret_str = str(self.id)
        cust_str = str(self.project_id) 
        return ret_str + ' | ' + cust_str

    def get_absolute_url(self):
        return reverse("client-details", args=(str(self.id)))
    
class Payments(models.Model):
    
    billing_id = models.ForeignKey(Billing, on_delete=models.CASCADE)
    amount = models.FloatField(default=5.00) 
    receipt = models.CharField(max_length=400, blank=True)
    time_stamp = models.DateField(auto_created=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, default='due')
    invoice_id = models.CharField(max_length=400, blank=True)
    
    def __str__(self):
        num_str = str(self.id)
        amount_str = str(self.amount) 
        return num_str + ' # - $' + amount_str

    def get_absolute_url(self):
        return reverse("payments", args=(str(self.id)))
    

    