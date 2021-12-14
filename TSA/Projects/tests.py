from django.test import TestCase, Client
import json

from django.urls import reverse

from .models import Project, Ticket, TicketDetail
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
        self.user4 = User.objects.create(username="userreq",
                                         email="req@req.com",
                                         password="req12345",
                                         is_active=True,
                                         area=User.REQUIREMENTS,
                                         is_leader=True)
        self.user4.set_password('req12345')
        self.user4.save()
        self.user5 = User.objects.create(username="userux",
                                         email="ux@ux.com",
                                         password="ux123456",
                                         is_active=True,
                                         area=User.UX,
                                         is_leader=True)
        self.user5.set_password('ux123456')
        self.user5.save()
        self.client1 = client.objects.create(name="Electroingeniería",
                                             address="Córdoba, Argentina")
        self.client1.save()
        self.client2 = client.objects.create(name="Carrefour",
                                             address="Av Colón 900, Córdoba, Argentina")
        self.client2.save()
        self.project1 = Project.objects.create(code_name='Carrefar',
                                               software_name='Cajero',
                                               software_version='2.3.5',
                                               active=True,
                                               owner=self.user2,
                                               client=self.client2)
        self.project1.save()
        self.ticket1 = Ticket.objects.create(state=Ticket.CLOSED,
                                             description="Se debe corregir los colores de fondo ya que son demasiado brillantes",
                                             title="Corrección de colores",
                                             project=self.project1,
                                             created_by=self.user4,
                                             area=User.UX)
        self.ticket1.save()
        self.ticketdetal1 = TicketDetail.objects.create(description="Se corrigieron los colores según el pedido del cliente",
                                                        title="Corrección aplicada",
                                                        ticket=self.ticket1,
                                                        user=self.user5)
        self.ticketdetal1.save()
        response = self.browser.post('/api/auth/login/', {'email': 'pml@pm.com', 'password': 'pml12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))

    def test_create_project(self):
        cnt = Project.objects.count()
        self.assertEqual(cnt, 1)
        proyecto = dict(code_name='RR_Elec',
                        software_name='ElectroRecursos',
                        software_version='1.0',
                        active=True,
                        owner=self.user1.id,
                        client=self.client1.id)
        response = self.browser.post(reverse('projects-list'), proyecto)
        self.assertEqual(response.status_code, 201)
        cnt = Project.objects.count()
        self.assertEqual(cnt, 2)


    def test_filter_projects(self):
        proyect = dict(code_name='RR_Elec',
                        software_name='ElectroRecursos',
                        software_version='1.0',
                        active=True,
                        owner=self.user1.id,
                        client=self.client1.id)
        self.browser.post(reverse('projects-list'),  proyect)
        cnt = Project.objects.count()
        self.assertEqual(cnt, 2)
        response = self.browser.get(reverse('projects-list'))
        self.assertEqual(len(response.data), 2)
        filters = dict(owner='', active='', client='')
        response = self.browser.post(reverse('filter_projects-list'), filters)
        self.assertEqual(response.status_code, 200)
        cnt = len(response.data)
        self.assertEqual(cnt, 2)
        filters = dict(owner=self.user1.id, active='', client='')
        response = self.browser.post(reverse('filter_projects-list'), filters)
        self.assertEqual(response.status_code, 200)
        cnt = len(response.data)
        self.assertEqual(cnt, 1)
        filters = dict(owner='', active='', client=self.client2.id)
        response = self.browser.post(reverse('filter_projects-list'), filters)
        self.assertEqual(response.status_code, 200)
        cnt = len(response.data)
        self.assertEqual(cnt, 1)
        filters = dict(owner='', active=True, client='')
        response = self.browser.post(reverse('filter_projects-list'), filters)
        self.assertEqual(response.status_code, 200)
        cnt = len(response.data)
        self.assertEqual(cnt, 2)
        filters = dict(owner='', active=False, client='')
        response = self.browser.post(reverse('filter_projects-list'), filters)
        self.assertEqual(response.status_code, 204)

    def test_create_tiket(self):
        idp = self.project1.id
        new_ticket = dict(state=Ticket.NEW,
                         description="Se debe corregir error en conteo de stock",
                         title="Corrección de stock",
                         project=idp,
                         created_by=self.user3.id,
                         area=User.MAINTENANCE)
        response = self.browser.post(reverse('tickets-list'), json.dumps(new_ticket), content_type="application/json")
        self.assertEqual(response.status_code, 403)
