from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from src.apps.backend.models import Post
from src.apps.backend.serializers import PostResponseSerializer


class PostView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = PostResponseSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        user = kwargs.get('username')
        queryset = super().get_queryset()
        queryset.filter(author__username=user)

        return Response(self.serializer_class(queryset, many=True).data)
