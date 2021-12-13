from rest_framework.routers import DefaultRouter

from .views import ProjectModelViewSet, FilterProjectModelViewSet

router_proj = DefaultRouter()

router_proj.register(prefix='projects', basename='projects',
                     viewset=ProjectModelViewSet)








router_proj.register(prefix='projects_filter', basename='filter_projects',
                     viewset=FilterProjectModelViewSet)
