from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from ckeditor.fields import RichTextField

    
class Blog(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    article = RichTextField(blank=True, null=True)
    group_id = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    preview = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, null=True)
    image_id = models.ForeignKey('gallery.Image', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.title) + ' | ' + str(self.user)
    
    def get_absolute_url(self):
        return reverse("post-details", args=(str(self.id)))