from django.db import models
from clients.models import Client
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserPayment(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    
@receiver(post_save, sender=Client)
def create_user_paymenty(sender,instance, created, **kwargs):
	if created:
		UserPayment.objects.create(client_id=instance)

	
