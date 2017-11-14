from django.contrib.auth.models import User
from django.db import models

class CmsUser(models.Model):
    user = models.OneToOneField(User)
    avatar = models.URLField(max_length=200,blank=True)