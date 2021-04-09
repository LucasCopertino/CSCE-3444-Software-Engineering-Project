
# Create your tests here.
from django.test import TestCase
from django.urls import reverse, resolve
from menu.views import menu_home, cat_g
from menu.models import category
from django.test import Client

class TestUrls(TestCase):
    def test_menu_url_is_resolved(self):
        url = reverse('menu_home')
        self.assertEquals(resolve(url).func, menu_home)
    def test_categtories_are_resolved(self):
        url = reverse('categories', args=[1])
        self.assertEquals(resolve(url).func, cat_g)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        category.objects.create(
            name='test category'
        )
    def test_menu_view(self):
        response = self.client.get(reverse('menu_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
    def test_categories_view(self):

        cat = category.objects.get(name="test category")
        response = self.client.get(reverse('categories', args=[cat.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')