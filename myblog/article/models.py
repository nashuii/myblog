from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class ArticleModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User,null=True)
    title = models.CharField(max_length=100)
    category = models.ForeignKey('CategoryModel')
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField(blank=True)
    tags = models.ManyToManyField('TagModel',blank=True)
    content_html = models.TextField()

class CategoryModel(models.Model):
    name = models.CharField(max_length=20,unique=True)

class TagModel(models.Model):
    name = models.CharField(max_length=20,unique=True)

class DiscussModel(models.Model):
    content = models.TextField()
    article = models.ForeignKey(ArticleModel)
    auth = models.ForeignKey(User)

class DiscussToDiscussModel(models.Model):
    content = models.TextField()
    discuss = models.ForeignKey(DiscussModel)
    auth = models.ForeignKey(User)