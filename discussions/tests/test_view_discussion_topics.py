from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Discussion
from ..views import discussion_topics

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
