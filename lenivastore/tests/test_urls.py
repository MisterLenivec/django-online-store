from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.test import TestCase, Client
from lenivastore.views import product_list, product_detail, about_project


# class TestUrls(SimpleTestCase):
#
#     def test_list_url_resolves(self):
#         url = reverse('product_list')
#         self.assertEquals(resolve(url).func, product_list)
#
#     def test_about_url_resolvers(self):
#         url = reverse('about_project')
#         self.assertEquals(resolve(url).func, about_project)
#
#     def test_basics_resolved(self):
#         a, b = 5, 3
#         res = a + b
#         self.assertEquals(res, 7)


class TestViews(TestCase):

    def test_project_list_GET(self):
        client = Client()

        response = client.get(reverse('about_project'))

        self.assertEquals(response.status_code, 200)
