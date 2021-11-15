from rest_framework.serializers import ModelSerializer
from client.models import Client, Contact


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['name','address']

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['client','name','phone','mail','is_main_contact']
