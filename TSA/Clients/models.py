from django.db import models

# Soy un puto promastercrack


class Client(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    mail = models.CharField(max_length=30)
    is_main_contact = models.BooleanField()
