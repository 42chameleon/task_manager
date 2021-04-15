from django.urls import path

from .views import CreateUserView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', CreateUserView.as_view(), name='registration'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
