from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Assignment
from .serializers import AssignmentSerializer
from accounts.permissions import IsTeacherOrPrincipal
from .models import AssignmentSubmission
from .serializers import AssignmentSubmissionSerializer,AssignmentReviewSerializer
from accounts.permissions import IsStudent
from .serializers import ParentAssignmentTrackerSerializer
from students.models import ParentStudent
from accounts.permissions import IsParent
# Create your views here.

class ParentAssignmentTrackerView(generics.ListAPIView):
    """
    GET /api/assignments/parent-tracker/
    Shows assignment submissions for all children linked to the parent.
    """
    serializer_class = ParentAssignmentTrackerSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get_queryset(self):
        parent = self.request.user
        linked_students = ParentStudent.objects.filter(parent=parent).values_list('student_id', flat=True)
        return AssignmentSubmission.objects.filter(student_id__in=linked_students)

class AssignmentSubmissionListView(generics.ListAPIView):
    """
    GET /api/assignments/<assignment_id>/submissions/
    Allows teacher/principal to view all submissions for a specific assignment.
    """
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrPrincipal]

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return AssignmentSubmission.objects.filter(assignment_id=assignment_id)

class AssignmentReviewView(generics.UpdateAPIView):
    """
    PATCH /api/assignments/review/<submission_id>/
    Allows teacher/principal to approve or reject a student submission.
    """
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrPrincipal]


class AssignmentSubmissionView(generics.CreateAPIView):
    """
    POST /api/assignments/submit/
    Allows students to submit assignment files.
    """
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    parser_classes = [MultiPartParser, FormParser]

    

class AssignmentCreateView(generics.CreateAPIView):
    """
    POST /api/assignments/upload/
    Allows teacher/principal to create assignments with file upload
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrPrincipal]
    parser_classes = [MultiPartParser, FormParser]

class AssignmentListView(generics.ListAPIView):
    """
    GET /api/assignments/
    Accessible by students, parents, teachers, principal
    Filters by subject or teacher if needed
    """
    queryset = Assignment.objects.select_related('subject', 'assigned_by')
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        subject_id = self.request.query_params.get('subject')
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        return qs
