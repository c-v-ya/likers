from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from backend.views.post import PostView
from backend.views.auth import SignUpView

posts_router = SimpleRouter()
posts_router.register(r"", PostView, basename="post")

app_name = "backend"
urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign_up"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain"),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("posts/", include(posts_router.urls)),
]
