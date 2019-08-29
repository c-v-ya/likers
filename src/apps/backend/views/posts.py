from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from src.apps.backend.models import Post
from src.apps.backend.serializers import (
    PostResponseSerializer,
    PostRequestSerializer,
)


class PostView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = PostResponseSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        user = kwargs.get('username')
        queryset = super().get_queryset()
        queryset.filter(author__username=user)

        return Response(self.serializer_class(queryset, many=True).data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['author_id'] = user.id
        serializer = PostRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()
