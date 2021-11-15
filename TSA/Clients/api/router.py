from rest_framework.routers import DefaultRouter
from Clients.api.views import  ClientViewSet, ContactViewSet

router_clients = DefaultRouter()
router_contacts = DefaultRouter()

router_clients.register(prefix='clients',basename='clients', viewset=ClientViewSet)
router_contacts.register(prefix='contacts',basename='contacts', viewset=ContactViewSet)