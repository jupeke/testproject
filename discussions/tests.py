from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home, discussion_topics #metodinkin voi näin tuoda.
from .models import Discussion

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

    def test_discussion_topics_url_resolves_board_discussions_view(self):
        view = resolve('/discussions/1/')
        self.assertEquals(view.func, discussion_topics)

    def test_discussion_topics_view_contains_link_to_home_page(self):
        topics_url = reverse('url_discussion_topics', kwargs={'discussion_id':1})
        response = self.client.get(topics_url)
        home_url = reverse('url_home')

        #{0} refers to the 1st param of format function.
        self.assertContains(response, 'href="{0}"'.format(home_url))
