from django.db import models
from accounts.models import User

# Create your models here.

class Standard(models.Model):
    name = models.CharField(max_length=20, unique=True) 

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=5) 
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="sections")

    def __str__(self):
        return f"{self.standard.name} - {self.name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    standard = models.ForeignKey(Standard, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()


class ParentStudent(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="parents")

    def __str__(self):
        return f"{self.parent.get_full_name()} ↔ {self.student.user.get_full_name()}"
    
class Attendance(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name="attendances"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("PRESENT", "Present"), ("ABSENT", "Absent")]
    )
    marked_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, related_name="attendance_marked"
    )


    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.standard.name})"