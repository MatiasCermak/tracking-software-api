from rest_framework.viewsets import ModelViewSet
from Clients.models import Client, Contact
from Clients.api.serializers import ClientSerializer, ContactSerializer
from .permissions import IsSalesOnly


class ClientModelViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsSalesOnly]


class ContactModelViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = [IsSalesOnly]

    def get_queryset(self):
        queryset = self.queryset
        client = self.request.query_params.get('client')

        if client is not None:
            queryset = queryset.filter(client=client)

        return queryset
