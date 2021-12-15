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
        fields = ['state', 'description', 'title',
                  'project', 'created_by', 'area', 'details']


class TicketModifySerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['description', 'title',
                  'project']#Corrobrar que se pueda cambiar el proyecto


class TicketChangeStateSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['state']


class TicketChangeAreaSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['area']


class ProjectSerializer(ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['code_name', 'software_name', 'software_version',
                  'active', 'owner', 'client', 'tickets']

   
class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['code_name', 'software_name', 'software_version', 'active', 'owner', 'client']


class ProjectFilterListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['active', 'owner', 'client']
