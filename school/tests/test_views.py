from django.test import TestCase
from django.urls import reverse


class StylesListViewTests(TestCase):
    def test_no_styles(self):
        response = self.client.get(reverse('school:styles_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['styles']), 0)