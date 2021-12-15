from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
import json

from django.urls import reverse

from .models import Project, Ticket, TicketDetail
from Users.models import User
from Clients.models import Client as client
from .api.serializers import ProjectListSerializer


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
        self.user6 = User.objects.create(username="useruxbase",
                                         email="uxb@uxb.com",
                                         password=make_password("uxb12345"),
                                         is_active=True,
                                         area=User.UX,
                                         is_leader=False)
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
        self.ticketdetal1 = TicketDetail.objects.create(description="Se ponderan opciones entre los colores preseleccionados",
                                                        title="Ponderando opciones",
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
        new_ticket = dict(state=Ticket.NEW,
                          description="Se debe corregir error en conteo de stock",
                          title="Corrección de stock",
                          project=idp,
                          created_by=self.user4.id,
                          area=User.MAINTENANCE)
        response = self.browser.post(reverse('tickets-list'), json.dumps(new_ticket), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        new_ticket = dict(state=Ticket.NEW,
                          description="Se debe corregir error en conteo de stock",
                          title="Corrección de stock",
                          project=idp,
                          created_by=self.user4.id,
                          area=User.REQUIREMENTS)
        response = self.browser.post(reverse('tickets-list'), json.dumps(new_ticket), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        response = self.browser.post('/api/auth/login/', {'email': 'req@req.com', 'password': 'req12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.post(reverse('tickets-list'), json.dumps(new_ticket), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_ticket_detail(self):
        new_detail = dict(description="Se realizó la corrección solicitada",
                          title="Corregido",
                          ticket=self.ticket1.id,
                          user=self.user4.id)
        response = self.browser.post(reverse('tickets_details-list'), json.dumps(new_detail),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 403)
        cnt = TicketDetail.objects.count()
        self.assertEqual(cnt, 1)
        response = self.browser.post('/api/auth/login/', {'email': 'req@req.com', 'password': 'req12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.post(reverse('tickets_details-list'), json.dumps(new_detail),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 403)
        new_detail = dict(description="Se realizó la corrección solicitada",
                          title="Corregido",
                          ticket=self.ticket1.id,
                          user=self.user5.id)
        response = self.browser.post(reverse('tickets_details-list'), json.dumps(new_detail),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 403)
        response = self.browser.post('/api/auth/login/', {'email': 'ux@ux.com', 'password': 'ux123456'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.post(reverse('tickets_details-list'), json.dumps(new_detail),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_change_project_data(self):
        project_serializer = ProjectListSerializer(Project.objects.last())
        response = self.browser.post('/api/auth/login/', {'email': 'ux@ux.com', 'password': 'ux123456'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        data = project_serializer.data
        data["owner"] = self.user1.id
        project_serializer = ProjectListSerializer(data=data)
        response = self.browser.patch(reverse('projects-detail', args=[self.project1.id]),
                                      json.dumps(project_serializer.initial_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        response = self.browser.post('/api/auth/login/', {'email': 'pmb@pm.com', 'password': 'pmb12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('projects-detail', args=[self.project1.id]),
                                      json.dumps(project_serializer.initial_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        data = project_serializer.initial_data
        data["owner"] = self.user2.id
        data["software_version"] = '2.3.7'
        project_serializer = ProjectListSerializer(data=data)
        response = self.browser.patch(reverse('projects-detail', args=[self.project1.id]),
                                      json.dumps(project_serializer.initial_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = project_serializer.initial_data
        data["owner"] = self.user1.id
        project_serializer = ProjectListSerializer(data=data)
        response = self.browser.post('/api/auth/login/', {'email': 'pml@pm.com', 'password': 'pml12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('projects-detail', args=[self.project1.id]),
                                      json.dumps(project_serializer.initial_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_change_ticket_state(self):
        state = dict(state=Ticket.IN_PROGRESS)
        response = self.browser.post('/api/auth/login/', {'email': 'req@req.com', 'password': 'req12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('tickets_state-detail', args=[self.ticket1.id]),
                           json.dumps(state), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        response = self.browser.post('/api/auth/login/', {'email': 'uxb@uxb.com', 'password': 'uxb12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('tickets_state-detail', args=[self.ticket1.id]),
                                      json.dumps(state), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        response = self.browser.post('/api/auth/login/', {'email': 'ux@ux.com', 'password': 'ux123456'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('tickets_state-detail', args=[self.ticket1.id]),
                                      json.dumps(state), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.ticket1 = Ticket.objects.get(pk=self.ticket1.id)
        self.assertEqual(self.ticket1.state, Ticket.IN_PROGRESS)

    def test_change_ticket_area(self):
        area = dict(area=User.MAINTENANCE)
        response = self.browser.post('/api/auth/login/', {'email': 'ux@ux.com', 'password': 'ux123456'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('tickets_area-detail', args=[self.ticket1.id]),
                                      json.dumps(area), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        response = self.browser.post('/api/auth/login/', {'email': 'pml@pm.com', 'password': 'pml12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('tickets_area-detail', args=[self.ticket1.id]),
                                      json.dumps(area), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.ticket1 = Ticket.objects.get(pk=self.ticket1.id)
        self.assertEqual(self.ticket1.area, User.MAINTENANCE)

    def test_modify_ticket(self):
        new_data = dict(description="Descripción cambiada",
                        title="Otro título")
        response = self.browser.post('/api/auth/login/', {'email': 'uxb@uxb.com', 'password': 'uxb12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        id_ticket = self.ticket1.id
        response = self.browser.patch(reverse('tickets-detail', args=[self.ticket1.id]),
                                      json.dumps(new_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        response = self.browser.post('/api/auth/login/', {'email': 'ux@ux.com', 'password': 'ux123456'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.patch(reverse('tickets-detail', args=[self.ticket1.id]),
                                      json.dumps(new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.ticket1 = Ticket.objects.get(pk=self.ticket1.id)
        self.assertEqual(self.ticket1.title, "Otro título")

    def test_list_tickets(self):
        response = self.browser.get(reverse('tickets-list'))
        self.assertEqual(len(response.data), 0)
        response = self.browser.post('/api/auth/login/', {'email': 'ux@ux.com', 'password': 'ux123456'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        response = self.browser.get(reverse('tickets-list'))
        self.assertEqual(len(response.data), 1)


