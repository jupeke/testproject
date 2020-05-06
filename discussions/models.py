from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

# Sub class of Model class:
class Discussion(models.Model):
    name = models.CharField(max_length=30, unique=True)

    description = models.CharField(max_length=100)

    def __str__(self):
        return "Discussion about " + self.name

    # Number of Posts related to this discussion:
    def get_posts_count(self):
        return Post.objects.filter(topic__discussion=self).count()

    # Number of Topics related to this discussion:
    def get_topics_count(self):
        return Topic.objects.filter(discussion=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__discussion=self).\
            order_by('-created_by').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE,
        related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='topics')
    views = models.PositiveIntegerField(default=0)  # <- here

    # Number of Replys related to this Topic (excludin the starter post):
    # Note: this can be done in another way: see view!
    def get_replies_count(self):
        return Post.objects.filter(topic=self).count()-1

    def __str__(self):
        return self.subject

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

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_mess(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(15)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
