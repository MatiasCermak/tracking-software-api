from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def get_or_none(**kwargs):
        try:
            return Client.objects.get(**kwargs)
        except Client.DoesNotExist:
            return None


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts', default=0)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    mail = models.CharField(max_length=30)
    is_main_contact = models.BooleanField()
