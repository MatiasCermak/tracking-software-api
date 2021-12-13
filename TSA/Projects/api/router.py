from rest_framework.routers import DefaultRouter

from .views import ProjectModelViewSet, TicketModelViewSet, TicketChangeAreaViewSet, TicketChangeStateViewSet, TicketDetailModelViewSet

router_proj = DefaultRouter()

router_proj.register(prefix='projects', basename='projects',
                     viewset=ProjectModelViewSet)
router_proj.register(prefix='tickets', basename='tickets',
                     viewset=TicketModelViewSet)
router_proj.register(prefix='tickets/area', basename='tickets/area',
                     viewset=TicketChangeAreaViewSet)
router_proj.register(prefix='tickets/state', basename='tickets/state',
                     viewset=TicketChangeStateViewSet)
router_proj.register(prefix='tickets/details', basename='tickets/details',
                     viewset=TicketDetailModelViewSet)
