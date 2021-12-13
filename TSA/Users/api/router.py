from django.urls import path, include
from .views import UserRegisterModelViewSet, UserChangeAttrModelViewSet, UserChangePasswordModelViewSet, UserChangeAreaModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router_users = DefaultRouter()

router_users.register(
    prefix='register', viewset=UserRegisterModelViewSet, basename='register')

router_users.register(prefix='chagearea', basename='changearea',
                      viewset=UserChangeAreaModelViewSet)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router_users.urls)),
    path('changeattr/', UserChangeAttrModelViewSet.as_view(
        {'patch': 'partial_update'}), name='changeattr'),
    path('changepassword/', UserChangePasswordModelViewSet.as_view(
        {'patch': 'partial_update'}), name='changepassword'),
]
