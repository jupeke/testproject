from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Discussion, Post, Topic
from ..views import reply_topic
from ..forms import PostForm

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
    def test_redirection(self):
        login_url = reverse('url_login')
        response = self.client.get(self.url)
        self.assertRedirects(response,
            '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/discussions/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_contains_form(self):  # <- new test
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_new_topic_view_contains_links(self):
        home_url = reverse('url_home')
        topics_url = reverse(
            'url_discussion_topics', kwargs={'discussion_id':self.discussion.pk})

        # {0} refers to the 1st param of format function.
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}"'.format(topics_url))

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, message textarea
        '''
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)

class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'hello, world!'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        topic_posts_url = reverse(
            'url_topic_posts',
            kwargs={
                'discussion_id': self.discussion.pk,
                'topic_id': self.topic.pk
            }
        )
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_topic_valid_post_data(self):
        self.assertEquals(Post.objects.count(), 2)

class InvalidReplyTopicTests(ReplyTopicTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': ''})
        self.response2 = self.client.post(self.url, {})

    def test_reply_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(Post.objects.count(), 1)

    def test_reply_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        form = self.response2.context.get('form')
        self.assertEquals(self.response2.status_code, 200)
        self.assertTrue(form.errors)
