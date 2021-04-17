from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer


class ProfileDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
