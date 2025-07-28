from rest_framework.urls import path
from .api_enpoints import (
     RegisterView,
     ActivationAccountView,
     PhoneLoginView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', ActivationAccountView.as_view(), name='activate'),
    path('login/', PhoneLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     
]