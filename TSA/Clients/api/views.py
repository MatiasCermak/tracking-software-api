from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from Clients.models import Client, Contact
from Clients.api.serializers import ClientSerializer, ContactSerializer

class ContactViewSet(ViewSet):
    def list(self, request):
        serializer = ContactSerializer(Contact.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ClientViewSet(ViewSet):
    def list(self, request):
        serializer = ClientSerializer(Client.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
