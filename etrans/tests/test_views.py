from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve
from ..views import home, details, new_program
from ..models import Company

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('etrans:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_home_url_resolves_home_view(self):
        view = resolve('/etrans/')
        self.assertEquals(view.func, home)

class BoardTopicsTests(TestCase):
    def setUp(self):
        self.company=Company.objects.create(company_name='Sogatra',  location = 'pk8', numero_telephone = '07635581', description='Best Transport.')
        url = reverse('etrans:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/etrans/')
        self.assertEquals(view.func, home)

class NewTopicTests(TestCase):
    def setUp(self):
        Company.objects.create(company_name='Sogatra', location = 'pk8', numero_telephone = '07635581', description='Best Transport.')

   # def test_new_topic_view_success_status_code(self):
    #    url = reverse('etrans:new_program', kwargs={'pk': 3})
    #    response = self.client.get(url)
    #    self.assertEquals(response.status_code, 200)

    #def test_new_topic_view_not_found_status_code(self):
    #    url = reverse('etrans:new_program', kwargs={'pk': 99})
    #    response = self.client.get(url)
    #    self.assertEquals(response.status_code, 404)

    #def test_new_topic_url_resolves_new_topic_view(self):
     #   view = resolve('/etrans/1/new/')
    #    self.assertEquals(view.func, new_program)

    #def test_new_topic_view_contains_link_back_to_board_topics_view(self):
    #    new_topic_url = reverse('etrans:new_program', kwargs={'pk': 1})
    #    board_topics_url = reverse('etrans:details', kwargs={'pk': 1})
    #    response = self.client.get(new_topic_url)
     #   self.assertContains(response, 'href="{0}"'.format(board_topics_url))
    