from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import (StudentRegistrationSerializer,
                          LinkParentSerializer,
                          AttendanceSerializer, AttendanceMarkSerializer)
from .models import (Student,ParentStudent,Section,Standard,
                     Attendance, Section,Subject)
from .serializers import StandardSerializer, SectionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import User
from rest_framework import status
from rest_framework.views import APIView
from .serializers import AttendanceDailySerializer, AttendanceSummarySerializer
from datetime import datetime
from django.db.models import Count, Q
import json
from .serializers import MarkSerializer
from .permissions import IsParentOrStudent
from performance.models import Exam,Mark

# Create your views here.

class StudentMarksListView(generics.ListAPIView):
    
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated, IsParentOrStudent]
    queryset = Mark.objects.select_related('subject', 'exam', 'student')

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, pk=student_id)
        
        self.check_object_permissions(self.request, student)
        qs = self.queryset.filter(student=student)

        exam_id = self.request.query_params.get('exam')
        subject_id = self.request.query_params.get('subject')
        if exam_id:
            qs = qs.filter(exam_id=exam_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        return qs.order_by('-exam__date', 'subject__name')


class MyMarksListView(generics.ListAPIView):
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated]
    queryset = Mark.objects.select_related('subject', 'exam','entered_by', 'student')

    def get_queryset(self):
        user = self.request.user
        student = getattr(user, 'student_profile', None)  
        if student:
            return self.queryset.filter(student=student).order_by('-exam__date', 'subject__name')

        from .models import ParentStudent
        children_ids = ParentStudent.objects.filter(parent=user).values_list('student_id', flat=True)
        student_id = self.request.query_params.get('student')
        if student_id and int(student_id) in set(children_ids):
            return self.queryset.filter(student_id=student_id).order_by('-exam__date', 'subject__name')

        return Mark.objects.none()


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


class StandardListCreateView(generics.ListCreateAPIView):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer
    permission_classes = [IsTeacher]

   


class SectionListCreateView(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsTeacher]


class AttendanceMarkView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceMarkSerializer
    parmission_classes = [IsAuthenticated,IsTeacher]
    permission_classes = []

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        
        serializer.is_valid(raise_exception=True)
        
        records = []
        if type(serializer.validated_data) == list:
            
            for item in serializer.validated_data:
                student_id = int(item["student_id"])
                date = item["date"]
                status_ = item["status"]
                
                attendance = Attendance.objects.filter(student_id=student_id, date=date).first()
                
                if attendance:
                    attendance.status = status_
                    
                    attendance.marked_by = request.user
                    attendance.save()
                else:
                    obj = Attendance.objects.create(
                        student_id=student_id,
                        date=date,
                        status=status_,
                        marked_by=request.user
                        )
                    records.append(obj)
        else :
            obj, created = Attendance.objects.update_or_create(
                                student_id=int(serializer.validated_data["student_id"]),
                                date=serializer.validated_data["date"],
                                defaults={"status": serializer.validated_data["status"], "marked_by": request.user})
            records.append(obj)
        return Response(AttendanceSerializer(records, many=True).data,status=status.HTTP_200_OK)
    
class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs["student_id"]
        if self.request.user.role == "STUDENT" and self.request.user.id != int(student_id):
            return Attendance.objects.none()
        return Attendance.objects.filter(student_id=student_id).order_by("-date")
    
class ClassAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        section_id = self.kwargs["section_id"]
        section = Section.objects.get(id=section_id)
        date = self.request.query_params.get("date")
        students = Student.objects.filter(section=section)
        if date:
            return Attendance.objects.filter(student__in=students, date=date)
        return Attendance.objects.filter(student__in=students).order_by("-date")
    
def calculate_percentage(present, total_days):
    if total_days == 0:
        return "0%"
    return f"{round((present / total_days) * 100, 2)}%"

class AttendanceReportPrincipalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        queryset = Attendance.objects.all()

        standard = request.query_params.get("standard")
        section = request.query_params.get("section")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        if standard:
            std = Standard.objects.get(name=standard)
            students = Student.objects.filter(standard=std)
            users = [student.user for student in students ]
            queryset = queryset.filter(student__in=students)
        if section:
            sec = Section.objects.filter(name=section)
            students = Student.objects.filter(section__in=sec)
            users = [student.user for student in students ]
            queryset = queryset.filter(student__in=students)
        if from_date and to_date:
            queryset = queryset.filter(date__range=[from_date, to_date])

        summary_data = []
        student_ids = queryset.values_list("student_id", flat=True).distinct()

        for sid in student_ids:
            student_records = queryset.filter(student_id=sid)
            if not student_records.exists():
                continue
            student = student_records.first().student
            total_days = student_records.count()
            total_present = student_records.filter(status="PRESENT").count()
            total_absent = student_records.filter(status="ABSENT").count()
            
            summary_data.append({
                "student_name": f'{student.user.first_name} {student.user.last_name}',
                "standard": student.standard.name,
                "section": student.section.name,
                "total_present": total_present,
                "total_absent": total_absent,
                "attendance_percentage": calculate_percentage(total_present, total_days)
            })

        total_students = len(student_ids)
        total_days = queryset.values("date").distinct().count()
        overall_present = queryset.filter(status="PRESENT").count()
        overall_percentage = calculate_percentage(overall_present, queryset.count())

        return Response({
            "summary": {
                "total_students": total_students,
                "total_days": total_days,
                "average_attendance": overall_percentage
            },
            "records": summary_data
        })
    
class AttendanceReportParentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        parent = request.user
        linked_students = [parent.student for parent in ParentStudent.objects.filter(parent=parent)]
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        data = []
        for student_ in linked_students:
            user_records = Attendance.objects.filter(student=student_)
            if from_date and to_date:
                user_records = user_records.filter(date__range=[from_date, to_date])

            if not user_records.exists():
                continue

            student_ = user_records.first().student
            student = student_
            total_days = user_records.count()
            total_present = user_records.filter(status="PRESENT").count()
            total_absent = user_records.filter(status="ABSENT").count()
            child_data = {
                "student_name": f'{student.user.first_name} {student.user.last_name}',
                "standard": student.standard.name,
                "section": student.section.name,
                "summary": {
                    "total_days": total_days,
                    "present": total_present,
                    "absent": total_absent,
                    "percentage": calculate_percentage(total_present, total_days)
                },
                "records": AttendanceDailySerializer(user_records, many=True).data
            }
            data.append(child_data)

        return Response({"children": data})