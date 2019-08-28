from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.backend.serializers import SignUpRequestSerializer


class SignUpView(APIView):
    # Allow only anonymous users
    permission_classes = [~IsAuthenticated, ]
    serializer_class = SignUpRequestSerializer

    def post(self, request):
        serializer = SignUpRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()
