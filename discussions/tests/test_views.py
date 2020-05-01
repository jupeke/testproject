from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from ..views import home, discussion_topics, new_topic #metodinkin voi näin tuoda.
from ..models import Discussion, Topic, Post
from ..forms import NewTopicForm

# Create your tests here.
class HomeTests(TestCase):
    def setUp(self):
        self.discussion = Discussion.objects.create(
                            name='Django', description='Django discussion')
        url = reverse('url_home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        fonction_to_serve_url = resolve('/').func
        self.assertEquals(fonction_to_serve_url, home)

    def test_home_view_contains_link_to_topics_page(self):
        discussion_topics_url = reverse(
            'url_discussion_topics', kwargs={'discussion_id': self.discussion.pk})
        self.assertContains(self.response, 'href="{0}"'.format(discussion_topics_url))

class DiscussionTopicsTests(TestCase):
    def setUp(self):
        Discussion.objects.create(name='Django', description='Django discussion')

    def test_discussion_topics_view_success_status_code(self):
        url = reverse('url_discussion_topics', kwargs={'discussion_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_discussion_topics_view_not_found_status_code(self):
        url = reverse('url_discussion_topics', kwargs={'discussion_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_discussion_topics_url_resolves_discussions_view(self):
        view = resolve('/discussions/1/')
        self.assertEquals(view.func, discussion_topics)

    def test_discussion_topics_view_contains_links(self):
        topics_url = reverse('url_discussion_topics', kwargs={'discussion_id':1})
        response = self.client.get(topics_url)
        home_url = reverse('url_home')
        new_topic_url = reverse('url_new_topic', kwargs={'discussion_id':1})

        #{0} refers to the 1st param of format function.
        self.assertContains(response, 'href="{0}"'.format(home_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

class NewTopicsTests(TestCase):
    def setUp(self):
        Discussion.objects.create(name='Django', description='Django discussion')
        User.objects.create_user(username='john', email='john@doe.com', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('url_new_topic', kwargs={'discussion_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('url_new_topic', kwargs={'discussion_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/discussions/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_links(self):
        url = reverse('url_new_topic', kwargs={'discussion_id':1})
        response = self.client.get(url)
        home_url = reverse('url_home')
        topics_url = reverse('url_discussion_topics', kwargs={'discussion_id':1})

        # {0} refers to the 1st param of format function.
        self.assertContains(response, 'href="{0}"'.format(home_url))
        self.assertContains(response, 'href="{0}"'.format(topics_url))

    def test_csrf(self):
        url = reverse('url_new_topic', kwargs={'discussion_id': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('url_new_topic', kwargs={'discussion_id': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('url_new_topic', kwargs={'discussion_id': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('url_new_topic', kwargs={'discussion_id': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):  # <- new test
        url = reverse('url_new_topic', kwargs={'discussion_id': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('url_new_topic', kwargs={'discussion_id': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
