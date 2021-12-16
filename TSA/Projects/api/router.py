from rest_framework.routers import DefaultRouter

from .views import ProjectModelViewSet, TicketModelViewSet, TicketChangeAreaViewSet, TicketChangeStateViewSet, \
    TicketDetailModelViewSet, FilterProjectModelViewSet, FilterTicketsModelViewSet

router_proj = DefaultRouter()

router_proj.register(prefix='projects', basename='projects',
                     viewset=ProjectModelViewSet)
router_proj.register(prefix='tickets', basename='tickets',
                     viewset=TicketModelViewSet)
router_proj.register(prefix='tickets_area', basename='tickets_area',
                     viewset=TicketChangeAreaViewSet)
router_proj.register(prefix='tickets_state', basename='tickets_state',
                     viewset=TicketChangeStateViewSet)
router_proj.register(prefix='tickets_details', basename='tickets_details',
                     viewset=TicketDetailModelViewSet)
router_proj.register(prefix='projects_filter', basename='filter_projects',
                     viewset=FilterProjectModelViewSet)
router_proj.register(prefix='tickets_filter', basename='filter_tickets',
                     viewset=FilterTicketsModelViewSet)
