from rest_framework.serializers import ModelSerializer
from client.models import Client, Contact


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['client', 'name', 'phone', 'mail', 'is_main_contact']


class ClientSerializer(ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['name','address']
