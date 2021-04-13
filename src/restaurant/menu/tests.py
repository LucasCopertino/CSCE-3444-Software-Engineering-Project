
# Create your tests here.
from django.test import TestCase
from django.urls import reverse, resolve
from menu.views import menu_home, cat_g
from menu.models import category, Item
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Customer
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
        self.user = User.objects.create_user('john','johnpassworD1!')

        category.objects.create(
            name='test category'
        )
        Item.objects.create(
            name='test item',
            price =5.00,
            description = "test",
            calory_info =40,
            cat =category.objects.filter(name='test category')[0],

        )

    
    def test_menu_view(self):
        self.client.login(username='john', password='johnpassworD1!')
    
        response = self.client.get(reverse('menu_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
    def test_categories_view(self):

        cat = category.objects.get(name="test category")
        response = self.client.get(reverse('categories', args=[cat.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
    def test_items_view(self):

        cat = Item.objects.get(name="test item")
        response = self.client.get(reverse('item_view', args=[cat.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_item_details.html')