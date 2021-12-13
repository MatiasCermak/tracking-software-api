from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, ProjectListSerializer, ProjectFilterListSerializer
from Users.models import User
from Clients.models import Client
from .permissions import IsPMOrSalesCreateOrOnlyList
from Projects.models import Project
from django.urls import reverse
from django.shortcuts import redirect


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


class FilterProjectModelViewSet(ModelViewSet):
    serializer_class = [ProjectSerializer, ProjectFilterListSerializer]
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        filters = ProjectFilterListSerializer(data=self.request.data)
        projects = Project.objects.all()
        # if filters.initial_data['owner'] == '' and filters.initial_data['client'] == '' and filters.initial_data['active'] == '':
        #     return redirect(reverse('projects-list'))
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
