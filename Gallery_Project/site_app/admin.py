from django.contrib import admin
from .models import Contact
from gallery.models import Image, Project, Print, ProjectEvents
from blog.models import Blog
from management.models import Crew, Coupon, Billing, Payments
from clients.models import Client, Invite, ProjectRequest, RequestReply, ProjectTerms

admin.site.register(Blog)
admin.site.register(Project)
admin.site.register(Image)
admin.site.register(Contact)
admin.site.register(Coupon)
admin.site.register(Crew)
admin.site.register(Client)
admin.site.register(Invite)
admin.site.register(Print)
admin.site.register(Billing)
admin.site.register(Payments)
admin.site.register(ProjectRequest)
admin.site.register(RequestReply)
admin.site.register(ProjectTerms)
admin.site.register(ProjectEvents)
