# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        if User.objects.filter(email=email).exists():
            return Response({
                'success': False,
                "message": "Email already exists."
            }, status=status.HTTP_200_OK)
        
        if User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                "message": "Username already exists."
            }, status=status.HTTP_200_OK)
        
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True,'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    "message": "User with this email does not exist"
                }, status=status.HTTP_200_OK)
            
            user = authenticate(username=user.username, password=password)

            if not user:
                return Response({
                    "message": "Incorrect password"
                }, status=status.HTTP_200_OK)

            if not user.is_active:
                return Response({
                    "message": "Your account is inactive"
                }, status=status.HTTP_200_OK)
            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "role": user.role,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
