from django.urls import resolve, reverse
from django.test import TestCase
from .views import detail
from .models import Pertanyaan


class BoardTopicsTests(TestCase):
    def setUp(self):
        Pertanyaan.objects.create(pertanyaan_text='Django')

    def test_board_topics_view_success_status_code(self):
        url = reverse('delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('detail', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/faq/1/')
        self.assertEquals(view.func, detail)
