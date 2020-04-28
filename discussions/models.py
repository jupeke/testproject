from django.db import models
from django.contrib.auth.models import User

# Sub class of Model class:
class Discussion(models.Model):
    name = models.CharField(max_length=30, unique=True)

    description = models.CharField(max_length=100)
    def __str__(self):
        return "Discussion about " + self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE,
        related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='topics')


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
        related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='posts')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
        null=True, related_name='+')
