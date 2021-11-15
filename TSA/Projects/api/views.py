from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, TicketSerializer, TicketDetailSerializer
from Users.api.serializers import UserSerializer
from Users.models import User
from Users.permissions import IsProjectManagerOrSalesCreate
from Projects.models import Project


class ProjectModelViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectManagerOrSalesCreate]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        if user.area == User.SALES or user.area == User.PROJECT_MANAGEMENT:
            project_serializer = ProjectSerializer(data=request.data)
            project_serializer.is_valid(raise_exception=True)
            project_serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=project_serializer.data)
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




    # def get_queryset(self):
    #     user = UserSerializer(data=self.request.user)
    #     user.is_valid(raise_exception=True)
    #     if user.validated_data["area"] == User.PROJECT_MANAGEMENT:
    #         return Project.objects.all()
    #     else
