from django.contrib import admin
from .models import Contact
from gallery.models import Image, Project, Print
from blog.models import Blog
from management.models import Crew, Coupon, Billing
from clients.models import Client 

admin.site.register(Blog)
admin.site.register(Project)
admin.site.register(Image)
admin.site.register(Contact)
admin.site.register(Coupon)
admin.site.register(Crew)
admin.site.register(Client)
admin.site.register(Print)
admin.site.register(Billing)

