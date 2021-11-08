from Projects.models import Project, Ticket, TicketDetail
from rest_framework.serializers import ModelSerializer


class TicketDetailSerializer(ModelSerializer):
    class Meta:
        model = TicketDetail
        fields = ['description', 'title', 'ticket', 'user']


class TicketSerializer(ModelSerializer):
    details = TicketDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['state', 'description', 'title', 'project', 'created_by', 'area']


class ProjectSerializer(ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        field = ['code_name', 'software_name', 'software_version', 'active', 'owner', 'client']
