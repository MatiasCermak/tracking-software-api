from rest_framework.routers import DefaultRouter
from .views import ProjectModelViewSet

router_proj = DefaultRouter()

router_proj.register(prefix='projects', basename='projects', viewset=ProjectModelViewSet)
