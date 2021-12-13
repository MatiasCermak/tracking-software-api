from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import rest_framework.status as status
from .serializers import UserRegisterSerializer, UserSerializer, UserChangeAttrSerializer, UserChangePasswordSerializer, UserChangeAreaSerializer
from Users.models import User
from .permissions import IsProjectManager
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action


class UserRegisterModelViewSet(ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = [IsProjectManager, ]

    def create(self, request, *args, **kwargs):
        if request.user.area != User.PROJECT_MANAGEMENT:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error : No tienes permisos para crear un usuario"})
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        serializer.validated_data['password'] = make_password(password)
        user = serializer.save()
        user.set_password(serializer.initial_data['password'])
        retSerializer = UserSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data=retSerializer.data)


class UserChangeAttrModelViewSet(ModelViewSet):
    serializer_class = UserChangeAttrSerializer
    queryset = []
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch']

    def partial_update(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        serializer = UserChangeAttrSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        saved_user = serializer.save()
        retSerializer = UserSerializer(saved_user)
        return Response(status=status.HTTP_200_OK, data=retSerializer.data)


class UserChangeAreaModelViewSet(ModelViewSet):
    serializer_class = UserChangeAreaSerializer
    queryset = []
    permission_classes = [IsProjectManager, ]
    http_method_names = ['patch']

    def partial_update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if request.user.area != User.PROJECT_MANAGEMENT:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error : No tienes permisos para cambiar el area a un usuario"})
        serializer = UserChangeAreaSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        saved_user = serializer.save()
        retSerializer = UserSerializer(saved_user)
        return Response(status=status.HTTP_200_OK, data=retSerializer.data)


class UserChangePasswordModelViewSet(ModelViewSet):
    serializer_class = UserChangePasswordSerializer
    queryset = []
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch']

    def partial_update(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        serializer = UserChangePasswordSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        serializer.validated_data['password'] = make_password(password)
        saved_user = serializer.save()
        retSerializer = UserSerializer(saved_user)
        return Response(status=status.HTTP_200_OK, data=retSerializer.data)
