from django.test import TestCase, Client
import json

from django.urls import reverse

from .models import Project
from Users.models import User
from Clients.models import Client as client


class ProjectTest(TestCase):
    def setUp(self):
        self.browser = Client()
        self.user1 = User.objects.create(username="pmleader",
                                          email="pml@pm.com",
                                          password="pml12345",
                                          is_active=True,
                                          area=User.PROJECT_MANAGEMENT,
                                          is_leader=True)
        self.user1.set_password('pml12345')
        self.user1.save()
        self.user2 = User.objects.create(username="pmbase",
                                          email="pmb@pm.com",
                                          password="pmb12345",
                                          is_active=True,
                                          area=User.PROJECT_MANAGEMENT,
                                          is_leader=False)
        self.user2.set_password('pmb12345')
        self.user2.save()
        self.user3 = User.objects.create(username="usersale",
                                          email="sale@sale.com",
                                          password="sale1234",
                                          is_active=True,
                                          area=User.SALES,
                                          is_leader=False)
        self.user3.set_password('sale1234')
        self.user3.save()
        self.client1 = client.objects.create(name="Electroingeniería",
                                             address="Córdoba, Argentina")
        self.client1.save()
        response = self.browser.post('/api/auth/login/', {'email': 'pml@pm.com', 'password': 'pml12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))

    def test_create_project(self):
        cnt = Project.objects.count()
        self.assertEqual(cnt, 0)
        proyecto = dict(code_name='RR_Elec',
                        software_name='ElectroRecursos',
                        software_version='1.0',
                        active=True,
                        owner=1,
                        client=1)
        response = self.browser.post(reverse('projects-list'), proyecto)
        self.assertEqual(response.status_code, 201)
        cnt = Project.objects.count()
        self.assertEqual(cnt, 1)


    def test_list_filter_projects(self):
        proyect = dict(code_name='RR_Elec',
                        software_name='ElectroRecursos',
                        software_version='1.0',
                        active=True,
                        owner=self.user1.id,
                        client=self.client1.id)
        self.browser.post(reverse('projects-list'),  proyect)
        cnt = Project.objects.count()
        self.assertEqual(cnt, 1)
        filters = dict(owner='', active='', client='')
        response = self.browser.post(reverse('filter_projects-list'), filters)
        self.assertEqual(response.status_code, 200)


