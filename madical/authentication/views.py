# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# helo
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            access_token = AccessToken.for_user(user)
            return Response({
                'access': str(access_token),
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "role": user.role,
                },
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
