from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from Clients.models import Client, Contact
from Clients.api.serializers import ClientSerializer, ContactSerializer


class ClientModelViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ContactModelViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    def get_queryset(self):
        queryset = self.queryset
        client = self.request.query_params.get('client')

        if client is not None:
            queryset = queryset.filter(client=client)

        return queryset


# class ContactByClientViewSet(ViewSet):
#     def retrieve(self, request, pk=None):
#         serializer = ContactSerializer(Contact.objects.filter(client=pk), many=True)
#         return Response(status=status.HTTP_200_OK, data=serializer.data)
#
# class ContactViewSet(ViewSet):
#     def list(self, request):
#         serializer = ContactSerializer(Contact.objects.all(), many=True)
#         return Response(status=status.HTTP_200_OK, data=serializer.data)
#
#     def clientContactList(self, request, client: int):
#         serializer = ContactSerializer(Contact.objects.all.filter(client=client), many=True)
#         return Response(status=status.HTTP_200_OK, data=serializer.data)
#
#     def retrieve(self, request, pk: int):
#         client = ContactSerializer(Contact.objects.get(pk=pk))
#         return Response(status=status.HTTP_200_OK, data=client.data)
#
#     #
#     # def list(self, request):
#     #     serializer = ContactSerializer(Contact.objects.all(), many=True)
#     #     return Response(status=status.HTTP_200_OK, data=serializer.data)
#
#     def create(self, request):
#         serializer = ContactSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_200_OK, data=serializer.data)
#
#
# class ClientViewSet(ViewSet):
#     def list(self, request):
#         serializer = ClientSerializer(Client.objects.all(), many=True)
#         return Response(status=status.HTTP_200_OK, data=serializer.data)
#
#     def retrieve(self, request, pk: int):
#         client = ClientSerializer(Client.objects.get(pk=pk))
#         return Response(status=status.HTTP_200_OK, data=client.data)
#
#     def create(self, request):
#         serializer = ClientSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_200_OK, data=serializer.data)



