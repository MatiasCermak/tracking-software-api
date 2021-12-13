from rest_framework.serializers import ModelSerializer
from Clients.models import Client, Contact


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'client', 'name', 'phone', 'mail', 'is_main_contact']


class ClientSerializer(ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'address', 'contacts']
