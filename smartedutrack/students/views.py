from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import (StudentRegistrationSerializer,
                          LinkParentSerializer)
from .models import Student,ParentStudent
# Create your views here.
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["teacher"]

class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [IsTeacher]


class LinkParentToStudentView(generics.CreateAPIView):
    queryset = ParentStudent.objects.all()
    serializer_class = LinkParentSerializer
    permission_classes = [IsTeacher]