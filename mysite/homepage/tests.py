import http

from django.test import TestCase


class HomepageTest(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_homepage_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "homepage/homepage.html")
        self.assertContains(response, "Главная")
