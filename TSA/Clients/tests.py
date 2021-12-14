from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from Users.models import User
from .models import Client as ClientModel, Contact

import json

class ClientTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="pmbase",
                                         email="pmb@pm.com",
                                         password=make_password("pmb12345"),
                                         is_staff=True,
                                         is_active=True,
                                         area=User.PROJECT_MANAGEMENT,
                                         is_leader=False)
        self.user1.save()
        self.user2 = User.objects.create(username="usersale",
                                         email="sale@sale.com",
                                         password=make_password("sale1234"),
                                         is_staff=True,
                                         is_active=True,
                                         area=User.SALES,
                                         is_leader=False)
        self.user2.save()

        self.browser = Client()
        self.client_test1 = ClientModel.objects.create(name='TestUser1',
                                                       address='Cordoba')
        self.client_test1.save()
        self.client_test2 = ClientModel.objects.create(name='TestUser2',
                                                       address='Cordoba')
        self.client_test2.save()

        client1 = self.client_test1.__dict__
        client2 = self.client_test2.__dict__
        del client1['_state']
        del client2['_state']
        client1['contacts'] = []
        client2['contacts'] = []
        self.j_client1 = json.dumps(client1)
        self.j_client2 = json.dumps(client2)

        response = self.browser.post(reverse('token_obtain_pair'), {'email': 'sale@sale.com', 'password': 'sale1234'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))

    def test_create_client(self):
        client = dict(name='TestUser3',
                      address='Chile')

        response = self.browser.post(reverse('clients-list'), client)
        self.assertEqual(response.status_code, 201)

    def test_get_clients(self):
        client_list = json.loads('[' + self.j_client1 + ',' + self.j_client2 + ']')
        response = self.browser.get(reverse('clients-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), client_list)

    def test_get_client_by_id(self):
        response = self.browser.get(reverse('clients-detail', args=[self.client_test1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), json.loads(self.j_client1))

    def test_put_client(self):
        client = dict(name='TestUser_Put',
                      address='TestUser4@123.com')

        client_new = json.loads(self.j_client1)

        client_new['name'] = client['name']
        client_new['address'] = client['address']

        response = self.browser.put(reverse('clients-detail', args=[self.client_test1.id]), client, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), client_new)

    def test_delete_client(self):
        response = self.browser.delete(reverse('clients-detail', args=[self.client_test1.id]))
        self.assertEqual(response.status_code, 204)


class ContactTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.browser = Client()

        self.user1 = User.objects.create(username="pmbase",
                                         email="pmb@pm.com",
                                         password=make_password("pmb12345"),
                                         is_staff=True,
                                         is_active=True,
                                         area=User.PROJECT_MANAGEMENT,
                                         is_leader=False)
        self.user1.save()
        self.user2 = User.objects.create(username="usersale",
                                         email="sale@sale.com",
                                         password=make_password("sale1234"),
                                         is_staff=True,
                                         is_active=True,
                                         area=User.SALES,
                                         is_leader=False)
        self.user2.save()

        self.client_test1 = ClientModel.objects.create(name='TestUser1',
                                                       address='Cordoba')
        self.client_test1.save()

        self.client_test2 = ClientModel.objects.create(name='TestUser2',
                                                       address='China')
        self.client_test2.save()

        self.contact_test1 = Contact.objects.create(client=self.client_test1,
                                                    name='TestContact1',
                                                    phone='111111111',
                                                    mail='TestContact1@123.com',
                                                    is_main_contact=True)
        self.contact_test1.save()

        self.contact_test2 = Contact.objects.create(client=self.client_test1,
                                                    name='TestContact2',
                                                    phone='222222222',
                                                    mail='TestContact2@123.com',
                                                    is_main_contact=True)
        self.contact_test2.save()
        self.contact_test3 = Contact.objects.create(client=self.client_test2,
                                                    name='TestContact3',
                                                    phone='333333333',
                                                    mail='TestContact3@123.com',
                                                    is_main_contact=True)
        self.contact_test3.save()
        contact1 = self.contact_test1.__dict__
        contact2 = self.contact_test2.__dict__
        contact3 = self.contact_test3.__dict__
        contact1['client'] = contact1['client_id']
        contact2['client'] = contact2['client_id']
        contact3['client'] = contact3['client_id']
        del contact1['_state']
        del contact2['_state']
        del contact3['_state']
        del contact1['client_id']
        del contact2['client_id']
        del contact3['client_id']
        self.j_contact1 = json.dumps(contact1)
        self.j_contact2 = json.dumps(contact2)
        self.j_contact3 = json.dumps(contact3)

        response = self.browser.post(reverse('token_obtain_pair'), {'email': 'sale@sale.com', 'password': 'sale1234'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))

    def test_create_contact(self):
        contact_test3 = dict(client=self.client_test1.id,
                             name='TestContact4',
                             phone='444444444',
                             mail='TestContact4@123.com',
                             is_main_contact=True)

        response = self.browser.post(reverse('contacts-list'), contact_test3)
        self.assertEqual(response.status_code, 201)

    def test_get_contacts(self):
        contacts_list = json.loads('[' + self.j_contact1 + ',' + self.j_contact2 + ',' + self.j_contact3 + ']')
        response = self.browser.get(reverse('contacts-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), contacts_list)

    def test_get_contact_by_id(self):
        response = self.browser.get(reverse('contacts-detail', args=[self.contact_test1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), json.loads(self.j_contact1))

    def test_get_contact_by_client(self):
        contacts_list = json.loads('[' + self.j_contact1 + ',' + self.j_contact2 + ']')
        response = self.browser.get(reverse('contacts-list') + '?client=' + str(self.client_test1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), contacts_list)

    def test_put_contact(self):
        contact = dict(client=self.client_test1.id,
                       name='TestContactPut',
                       phone='444444444',
                       mail='TestContact1@123.com',
                       is_main_contact=True)

        contact_new = json.loads(self.j_contact1)

        contact_new['name'] = contact['name']
        contact_new['phone'] = contact['phone']

        response = self.browser.put(reverse('contacts-detail', args=[self.contact_test1.id]), contact,
                                    'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), contact_new)

    def test_delete_contact(self):
        response = self.browser.delete(reverse('contacts-detail', args=[self.contact_test1.id]))
        self.assertEqual(response.status_code, 204)

