from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from accounts.permissions import IsTeacherOrPrincipal,IsPrincipal
from students.models import Student
from performance.models import Mark
from rest_framework import generics
from django.db.models import Avg

# Create your views here.

class ReportCardView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrPrincipal]

    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        marks = Mark.objects.filter(student=student)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_card_{student_id}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, f"Report Card - {student.user.get_full_name()}")
        y = 760
        for mark in marks:
            p.drawString(100, y, f"{mark.subject.name}: {mark.marks_obtained}")
            y -= 20
        p.showPage()
        p.save()

        return response
    
class ClassPerformanceView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsPrincipal]

    def list(self, request):
        data = (
            Mark.objects
            .values('student__standard__name')
            .annotate(avg_marks=Avg('marks_obtained'))
            .order_by('student__standard__name')
        )
        return Response(data)


class TopPerformersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsPrincipal]

    def list(self, request):
        toppers = (
            Mark.objects
            .values('student__id', 'student__user__first_name', 'student__standard__name')
            .annotate(avg_marks=Avg('marks_obtained'))
            .order_by('-avg_marks')[:3]
        )
        return Response(toppers)




