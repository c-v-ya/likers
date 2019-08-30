from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from src.apps.backend import views

app_name = 'backend'
urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),

    path('<str:username>/posts/<int:pk>/like/', views.like, name='post_like'),
    path('<str:username>/posts/<int:pk>/unlike/', views.unlike,
         name='post_unlike'),
    path('<str:username>/posts/<int:pk>/', views.post, name='post_retrieve'),
    path('<str:username>/posts/', views.post, name='post_list'),
    path('posts/', views.post, name='post_create'),
]
