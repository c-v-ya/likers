from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.backend.serializers import SignUpRequestSerializer


class SignUpView(views.APIView):
    # Allow only anonymous users
    permission_classes = [
        ~IsAuthenticated,
    ]
    serializer_class = SignUpRequestSerializer

    @swagger_auto_schema(operation_description='Sign Up')
    def post(self, request):
        serializer = SignUpRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()
