from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import CreateUserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SessionLoginSerializer

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
# Create your views here.

class CreateTeacherParentView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class SessionLoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = SessionLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)  
            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class SessionLogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)



class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://127.0.0.1:8000/api/accounts/password-reset-confirm/?uid={uid}&token={token}"

        return Response(
            {"message": "Password reset link generated", "reset_link": reset_link},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
