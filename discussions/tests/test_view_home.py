from django.urls import resolve, reverse
from django.test import TestCase
from ..views import home #metodinkin voi näin tuoda.
from ..models import Discussion

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
