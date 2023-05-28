from enum import Enum
from typing import Literal

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import Post
from backend.serializers.post import (
    PostResponseSerializer,
    PostRequestSerializer,
)


class Action(Enum):
    like = "like"
    unlike = "unlike"


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related("liked_by")
    serializer_class = PostResponseSerializer
    http_method_names = ("get", "post")

    @swagger_auto_schema(
        operation_description="Create post",
        request_body=PostRequestSerializer(),
        responses={200: PostResponseSerializer()},
    )
    def create(self, request, *args, **kwargs):
        self.serializer_class = PostRequestSerializer
        return super(PostView, self).create(request, *args, **kwargs)

    @swagger_auto_schema(
        method="get",
        operation_description="Like post",
        responses={200: ""},
    )
    @action(methods=["get"], detail=True, url_path="like", url_name="like")
    def like(self, request, *args, **kwargs):
        return self._post_action(Action.like, request, **kwargs)

    @swagger_auto_schema(
        method="get",
        operation_description="Unlike post",
        responses={200: ""},
    )
    @action(methods=["get"], detail=True, url_path="unlike", url_name="unlike")
    def unlike(self, request, *args, **kwargs):
        return self._post_action(Action.unlike, request, **kwargs)

    @staticmethod
    def _post_action(post_action: Literal[Action.like, Action.unlike], request, **kwargs):
        post_id = kwargs.get("pk")
        user = request.user
        post = get_object_or_404(Post.objects.exclude(author=user), id=post_id)
        if post_action == Action.unlike:
            post.liked_by.remove(user)
        else:
            post.liked_by.add(user)

        return Response(status=status.HTTP_200_OK)
