from rest_framework import serializers
from .models import Assignment
from students.models import Subject
from .models import AssignmentSubmission
from django.utils import timezone


class ParentAssignmentTrackerSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    due_date = serializers.DateField(source='assignment.due_date', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment_title', 'student_name',
            'submitted_at', 'status', 'remarks', 'due_date'
        ]

class AssignmentReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'status', 'remarks']
        read_only_fields = ['assignment', 'student']

    def validate_status(self, value):
        if value not in ['APPROVED', 'REJECTED']:
            raise serializers.ValidationError("Status must be APPROVED or REJECTED.")
        return value

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'file', 'submitted_at','status']
        read_only_fields = ['student', 'submitted_at']

    def validate(self, attrs):
        assignment = attrs['assignment']
        student = self.context['request'].user

        
        today = timezone.now().date()
        if assignment.due_date and assignment.due_date < today:
            raise serializers.ValidationError("Assignment is past due date.")

        
        if AssignmentSubmission.objects.filter(assignment=assignment, student=student).exists():
            raise serializers.ValidationError("You have already submitted this assignment.")
        
        return attrs

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)


class AssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    assigned_by_name = serializers.ReadOnlyField(source='assigned_by.get_full_name')

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'subject', 'subject_name',
            'assigned_by', 'assigned_by_name', 'file', 'due_date', 'created_at'
        ]
        read_only_fields = ['assigned_by', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['assigned_by'] = user
        return super().create(validated_data)
