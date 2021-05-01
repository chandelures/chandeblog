from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from userprofile.serializers import UserProfileSerializer


User = get_user_model()


class Logout(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserProfileList(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = UserProfileSerializer


class UserProfileDetail(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def get_serializer(self, instance, *args, **kwargs):
        return self.serializer_class(instance, *args, **kwargs)

    def get_object(self, request):
        instance = User.objects.get(pk=request.user.pk)
        return instance

    def get(self, request):
        user = self.get_object(request)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = self.get_object(request)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserProfileCreate(CreateAPIView):
    serializer_class = UserProfileSerializer
