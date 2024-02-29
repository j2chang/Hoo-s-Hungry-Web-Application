from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class URLtests(TestCase):
    def test_superuser_url(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_index_url(self):
        response = self.client.get('//')
        self.assertEqual(response.status_code, 200)

    def test_user_home(self):
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)

    def test_admin_home(self):
        response = self.client.get('/restaurantAdmin/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_survey_url(self):
        response = self.client.get('/survey/')
        self.assertEqual(response.status_code, 200)

    def test_categories_url(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)

    def test_map_url(self):
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)

#tests are currently passing but not sure if they are testing exactly what we think theyre testing
class GoogleLoginTest(TestCase):
    def setup(self):
        credentials = {"username": "testuser", "password": "testpw"}
        self.credentials = credentials
        User.objects.create_user(self.credentials)

    def testUserLogin(self):
        self.setup()
        response = self.client.get('/user/', self.credentials, follow=True)
        self.assertTrue(response.status_code == 200)

    def testAdminLogin(self):
        self.setup()
        response = self.client.get('/restaurantAdmin/', self.credentials, follow = True)
        self.assertTrue(response.status_code == 200)