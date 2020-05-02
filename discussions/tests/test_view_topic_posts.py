from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Discussion, Post, Topic
from ..views import topic_posts


class TopicPostsTests(TestCase):
    def setUp(self):
        d = Discussion.objects.create(name='Django', description='Django discussion.')
        user = User.objects.create_user(
            username='john', email='john@doe.com', password='123'
        )
        topic = Topic.objects.create(subject='Hello, world', discussion=d, starter=user)
        Post.objects.create(
            message='Lorem ipsum dolor sit amet', topic=topic, created_by=user
        )
        url = reverse('url_topic_posts',
            kwargs={'discussion_id': d.pk, 'topic_id': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/discussions/1/topics/1/')
        self.assertEquals(view.func, topic_posts)
