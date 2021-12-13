from rest_framework import response
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Clients.models import Client
from .serializers import ProjectSerializer, ProjectListSerializer, ProjectFilterListSerializer, TicketChangeAreaSerializer, TicketChangeStateSerializer, TicketModifySerializer, TicketSerializer, TicketDetailSerializer
from Users.models import User
from Users.api.permissions import IsProjectManager
from Projects.models import Project, Ticket
from .permissions import IsPMOrSalesCreateOrOnlyList, TicketChangeStateViewSetPermissions, TicketModelViewsetPermissions


class ProjectModelViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsPMOrSalesCreateOrOnlyList]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        if user.area == User.SALES or user.area == User.PROJECT_MANAGEMENT:
            client = Client.objects.get(pk=request.data['client'])
            owner = User.objects.get(pk=request.data['owner'])
            project = Project.objects.create(code_name=self.request.data['code_name'],
                                             software_name=self.request.data['software_name'],
                                             software_version=self.request.data['software_version'],
                                             active=self.request.data['active'],
                                             owner=owner, client=client)
            return Response(status=status.HTTP_201_CREATED, data=ProjectSerializer(project).data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario no tiene permisos para crear un nuevo proyecto"})

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        if user.area == User.PROJECT_MANAGEMENT:
            instance = self.get_object()
            instance.active = False
            instance.save()
            return Response(status=status.HTTP_200_OK, data=ProjectSerializer(instance))
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario no tiene permisos para modificar el proyecto"})

    def update(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        project_serializer = ProjectSerializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)
        project_bd = Project.objects.get(pk=project_serializer.initial_data['id'])
        if project_serializer.validated_data['owner'] != project_bd.owner \
                and (user.area != User.PROJECT_MANAGEMENT or (user.area == User.PROJECT_MANAGEMENT and not user.is_leader)):
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario debe ser líder del área de Project Management para asignar un dueño al projecto"})
        elif project_serializer.validated_data['owner'] != user:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario debe ser dueño del projecto para poder hacer modificaciones"})
        else:
            project_serializer.save()
            return Response(status=status.HTTP_200_OK, data=project_serializer.data)

          
class TicketModelViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [TicketModelViewsetPermissions]
    http_method_names = ['post', 'patch', 'get', 'delete']

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.pk)
        if user.area != User.PROJECT_MANAGEMENT or user.is_leader:
            return Ticket.objects.filter(area=user.area)
        else:
            return Ticket.objects.all()

    def create(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        ticket_serializer = TicketSerializer(data=request.data)
        ticket_serializer.is_valid(raise_exception=True)
        if user.area != ticket_serializer.data["area"] and user.area != User.PROJECT_MANAGEMENT:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario debe ser project manager o líder de área del área en la cual el ticket se va a crear."})
        else:
            ticket_serializer.save()
            return response(status=status.HTTP_201_CREATED, data=ticket_serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        ticket = Ticket.objects.get(pk=pk)
        user = User.objects.get(pk=request.user.pk)
        ticket_modify_serializer = TicketModifySerializer(
            instance=ticket, data=request.data, partial=True)
        ticket_modify_serializer.is_valid(raise_exception=True)
        if user.area != ticket_modify_serializer.data["area"] and user.area != User.PROJECT_MANAGEMENT:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario debe ser project manager o líder de área del área en la cual el ticket se va a modificar."})
        else:
            ticket_modify_serializer.save()
            ticket_modify_serializer = TicketSerializer(ticket)
            ticket_modify_serializer.is_valid(raise_exception=True)
            return response(status=status.HTTP_200_OK, data=ticket_modify_serializer.data)


class TicketChangeStateViewSet(ModelViewSet):
    serializer_class = TicketChangeStateSerializer
    permission_classes = [TicketChangeStateViewSetPermissions]
    http_method_names = ['patch']

    def partial_update(self, request, pk=None, *args, **kwargs):
        ticket = Ticket.objects.get(pk=pk)
        user = User.objects.get(pk=request.user.pk)
        ticket_change_state_serializer = TicketModifySerializer(
            instance=ticket, data=request.data, partial=True)
        ticket_change_state_serializer.is_valid(raise_exception=True)
        if user.area != ticket.area and user.area != User.PROJECT_MANAGEMENT:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario debe ser project manager o líder de área del área en la cual el ticket se encuentra."})
        else:
            ticket_change_state_serializer.save()
            ticket_serializer = TicketSerializer(ticket)
            ticket_serializer.is_valid(raise_exception=True)
            return response(status=status.HTTP_200_OK, data=ticket_serializer.data)


class TicketChangeAreaViewSet(ModelViewSet):
    serializer_class = TicketChangeAreaSerializer
    permission_classes = [IsProjectManager]
    http_method_names = ['patch']

    def partial_update(self, request, pk=None, *args, **kwargs):
        ticket = Ticket.objects.get(pk=pk)
        ticket_change_state_serializer = TicketModifySerializer(
            instance=ticket, data=request.data, partial=True)
        ticket_change_state_serializer.is_valid(raise_exception=True)
        ticket_change_state_serializer.save()
        ticket_serializer = TicketSerializer(ticket)
        ticket_serializer.is_valid(raise_exception=True)
        return response(status=status.HTTP_200_OK, data=ticket_serializer.data)


class TicketDetailModelViewSet(ModelViewSet):
    serializer_class = TicketDetailSerializer
    permission_classes = [TicketModelViewsetPermissions]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        ticket_detail_serializer = TicketDetailSerializer(
            data=request.data)
        ticket_detail_serializer.is_valid(raise_exception=True)
        try:
            ticket = Ticket.objects.get(
                pk=ticket_detail_serializer.data["ticket"])
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,  data={"error : El ticket referenciado por este detalle no fue encontrado"})
        if user.area != ticket.area and user.area != User.PROJECT_MANAGEMENT:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"error : El usuario debe ser project manager o líder de área del área a la cual el detalle de ticket pertenece"})
        else:
            ticket_detail_serializer.save()
            return response(status=status.HTTP_200_OK, data=ticket_detail_serializer.data)


class FilterProjectModelViewSet(ModelViewSet):
    serializer_class = [ProjectSerializer, ProjectFilterListSerializer]
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        filters = ProjectFilterListSerializer(data=self.request.data)
        projects = Project.objects.all()
        if filters.initial_data['owner'] != '':
            owner = User.get_or_none(pk=filters.initial_data['owner'])
            projects = projects.filter(owner=owner)
        if filters.initial_data['client'] != '':
            client = Client.get_or_none(pk=filters.initial_data['client'])
            projects = projects.filter(client=client)
        if filters.initial_data['active'] != '':
            active = filters.initial_data['active']
            projects = projects.filter(active=active)

        if projects.count() > 0:
            projects_list_serializer = ProjectListSerializer(projects, many=True)
            return Response(status=status.HTTP_200_OK, data=projects_list_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT, data={"error: La búsqueda no devolvió ningún valor"})
