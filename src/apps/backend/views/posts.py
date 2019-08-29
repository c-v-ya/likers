from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from src.apps.backend.models import Post
from src.apps.backend.serializers import (
    PostResponseSerializer,
    PostRequestSerializer,
)


class PostView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = PostResponseSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = kwargs.get('username')
        queryset = Post.objects.filter(author__username=user)

        return Response(self.serializer_class(queryset, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        user = kwargs.get('username')
        post_id = kwargs.get('pk')
        queryset = Post.objects.filter(author__username=user, id=post_id)
        post = get_object_or_404(queryset)

        return Response(self.serializer_class(post).data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['author_id'] = user.id
        serializer = PostRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()
