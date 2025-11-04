from django.db import models
from django.conf import settings
from students.models import Student, Subject
# Create your models here.

User = settings.AUTH_USER_MODEL


def assignment_upload_path(instance, filename):
    return f"assignments/{instance.subject.name}/{filename}"


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_assignments')
    file = models.FileField(upload_to=assignment_upload_path, blank=True, null=True)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.subject})"

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        unique_together = ('assignment', 'student')  

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"