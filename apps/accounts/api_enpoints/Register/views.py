from django.contrib.auth import get_user_model
from rest_framework.response import Response    
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ActivationSerializer
from apps.accounts.utils import send_sms_code, check_code
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()
class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        

        # Create user but mark as inactive
        user = serializer.save(is_active=False)

        # Send SMS code
        send_sms_code(user.phone)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivationAccountView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        # Check code
        success, message = check_code(phone, code)
        if not success:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        # Activate user
        try:
            user = User.objects.get(phone=phone)
            user.is_active = True
            user.save()
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)

__all__ = [
    'RegisterView',
    'ActivationAccountView'
]
    
    