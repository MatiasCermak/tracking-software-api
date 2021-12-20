from django.test import TestCase, Client
import json
from django.contrib.auth.hashers import make_password
from django.urls import reverse
import rest_framework
from rest_framework import response

from .models import User


class UserTest(TestCase):
    def setUp(self):
        self.browser = Client()
        self.client = User.objects.create(username="pepe",
                                          email='pepe@pepe.com',
                                          password=make_password("pepe123"),
                                          is_staff=True,
                                          is_active=True,
                                          area=0,
                                          is_leader=False)
        self.client.save()
        self.client2 = User.objects.create(username="user2",
                                           email='user2@user2.com',
                                           password=make_password("user123"),
                                           is_staff=True,
                                           is_active=True,
                                           area=2,
                                           is_leader=False)
        self.client2.save()
        response = self.browser.post(
            reverse('token_obtain_pair'), {'email': 'pepe@pepe.com', 'password': 'pepe123'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(
            rj.get('access'))

    def test_api_list_users(self):
        response = self.browser.get(reverse("users-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_api_add_user(self):
        user = dict(username='tom',
                    password='tom12345',
                    email='tom@admin.api',
                    first_name='Tomás',
                    last_name='Ferreyra')
        response = self.browser.post(reverse('register-list'), user)
        self.assertEqual(response.status_code, 201)

    def test_change_attr_user(self):
        new_data = dict(username='Pepo',
                        first_name=self.client.first_name,
                        last_name=self.client.last_name)
        response = self.browser.patch(reverse('changeattr'), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_change_pass_user(self):
        new_data = dict(password='pepe1234')
        response = self.browser.patch(reverse('changepassword'), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        rsp = self.browser.post(
            reverse('token_obtain_pair'), {'email': 'pepe@pepe.com', 'password': 'pepe1234'})
        self.assertEqual(rsp.status_code, 200)

    def test_change_area_user(self):
        new_data = dict(area=3)
        response = self.browser.patch(reverse('changearea-detail', kwargs={'pk': User.objects.last().id}), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['area'], 3)


class UserNotLeaderTest(TestCase):
    def setUp(self):
        self.browser = Client()
        self.client = User.objects.create(username="pepe",
                                          email='pepe@pepe.com',
                                          password=make_password("pepe123"),
                                          is_staff=True,
                                          is_active=True,
                                          area=2,
                                          is_leader=False)
        self.client.save()
        self.client = User.objects.create(username="user2",
                                          email='user2@user2.com',
                                          password=make_password("user123"),
                                          is_staff=True,
                                          is_active=True,
                                          area=2,
                                          is_leader=False)
        self.client.save()
        response = self.browser.post(
            reverse('token_obtain_pair'), {'email': 'pepe@pepe.com', 'password': 'pepe123'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(
            rj.get('access'))

    def test_api_list_users(self):
        response = self.browser.get(reverse("users-list"))
        self.assertEqual(response.status_code, 403)

    def test_api_add_user(self):
        user = dict(username='tom',
                    password='tom12345',
                    email='tom@admin.api',
                    first_name='Tomás',
                    last_name='Ferreyra')
        response = self.browser.post(reverse('register-list'), user)
        self.assertEqual(response.status_code, 403)

    def test_change_attr_user(self):
        new_data = dict(username='Pepo',
                        first_name=self.client.first_name,
                        last_name=self.client.last_name)
        response = self.browser.patch(reverse('changeattr'), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_change_pass_user(self):
        new_data = dict(password='pepe1234')
        response = self.browser.patch(reverse('changepassword'), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        rsp = self.browser.post(
            reverse('token_obtain_pair'), {'email': 'pepe@pepe.com', 'password': 'pepe1234'})
        self.assertEqual(rsp.status_code, 200)

    def test_change_area_user(self):
        new_data = dict(area=3)
        response = self.browser.patch(reverse('changearea-detail', kwargs={'pk': User.objects.last().id}), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.last().area, 2)

    def test_change_leader_attr(self):
        new_data = dict(is_leader=True)
        response = self.browser.patch(reverse('changeleaderattr-detail', kwargs={'pk': User.objects.last().id}), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.last().is_leader, False)


class UserLeaderTest(TestCase):
    def setUp(self):
        self.browser = Client()
        self.user1 = User.objects.create(username="pmleader",
                                         email="pml@pm.com",
                                         password=make_password("pml12345"),
                                         is_active=True,
                                         area=User.PROJECT_MANAGEMENT,
                                         is_leader=True)
        self.user1.save()
        self.user2 = User.objects.create(username="pmbase",
                                         email="pmb@pm.com",
                                         password=make_password("pmb12345"),
                                         is_active=True,
                                         area=User.PROJECT_MANAGEMENT,
                                         is_leader=False)
        self.user2.save()
        self.user3 = User.objects.create(username="usersale",
                                         email="sale@sale.com",
                                         password=make_password("sale1234"),
                                         is_active=True,
                                         area=User.SALES,
                                         is_leader=False)
        self.user3.save()
        response = self.browser.post(
            reverse('token_obtain_pair'), {'email': 'pml@pm.com', 'password': 'pml12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(
            rj.get('access'))

    def test_change_leader_attr(self):
        new_data = dict(is_leader=True)
        response = self.browser.patch(reverse('changeleaderattr-detail', kwargs={'pk': User.objects.last().id}), json.dumps(
            new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.last().is_leader, True)
