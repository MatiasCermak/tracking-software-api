from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .serializers import ProjectSerializer, TicketSerializer, TicketDetailSerializer


class ProjectModelViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        area = self.request.user.area
