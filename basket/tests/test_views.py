from django.test import TestCase
from django.urls import reverse

from authentication.models import MyUser
from school.models import Category, Abonement


class TestBasketView(TestCase):
    def setUp(self):
        user = MyUser.objects.create_user(username='test', email='test@mail.com', password='12345')
        user.is_active = True
        user.save()
        cat = Category.objects.create(name='Cat', salary=100.0)
        Abonement.objects.create(category=cat, number_of_lessons=4, price=400.0, duration=30)
        Abonement.objects.create(category=cat, number_of_lessons=8, price=800.0, duration=30)
        Abonement.objects.create(category=cat, number_of_lessons=16, price=1600.0, duration=30)

        self.client.post(
            reverse('basket:basket_add'), {'productid': 1, 'productqty': 1, 'action': 'post'}, xhr=True
        )
        self.client.post(
            reverse('basket:basket_add'), {'productid': 2, 'productqty': 2, 'action': 'post'}, xhr=True
        )

    def test_basket_url(self):
        response = self.client.get(reverse('basket:basket'))
        self.assertEqual(response.status_code, 302)

        self.client.post(reverse('auth:login'), {'username': 'test', 'password': '12345'})
        response = self.client.get(reverse('basket:basket'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'quantity': 4})

        response = self.client.post(
            reverse('basket:basket_add'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'quantity': 3})

    def test_basket_delete(self):
        response = self.client.post(
            reverse('basket:basket_delete'), {"productid": 2, "action": "delete"}, xhr=True)
        self.assertEqual(response.json(), {'quantity': 1, 'total': '400'})

    def test_basket_update(self):
        response = self.client.post(
            reverse('basket:basket_update'), {"productid": 2, "productqty": 1, "action": "update"}, xhr=True)
        self.assertEqual(response.json(), {'quantity': 2, 'total': '1200'})
