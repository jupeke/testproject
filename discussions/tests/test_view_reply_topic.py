from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Discussion, Post, Topic
from ..views import reply_topic

class ReplyTopicTestCase(TestCase):
    '''
    Base test case to be used in all `reply_topic` view tests
    '''
    def setUp(self):
        self.discussion = Discussion.objects.create(
            name='Django', description='Django discussion.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(
            username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(
            subject='Hello, world', discussion=self.discussion, starter=user)
        Post.objects.create(
            message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse(
            'url_reply_topic',
            kwargs={'discussion_id': self.discussion.pk, 'topic_id': self.topic.pk})

class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    # ...

class ReplyTopicTests(ReplyTopicTestCase):
    # ...

class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    # ...

class InvalidReplyTopicTests(ReplyTopicTestCase):
    # ...
