from django.urls import path
from . import views 
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name="student-register"),
    path('link-parent/', views.LinkParentToStudentView.as_view(), name="link-parent-student"),
    path("standards/", views.StandardListCreateView.as_view(), name="standard_list_create"),
    path("sections/", views.SectionListCreateView.as_view(), name="section_list_create"),

    path("attendance/mark/",csrf_exempt( views.AttendanceMarkView.as_view()), name="attendance_mark"),
    
    path("attendance/student/<int:student_id>/", views.StudentAttendanceView.as_view(), 
                                                 name="attendance_student"),
    path("attendance/class/<int:section_id>/", views.ClassAttendanceView.as_view(), 
                                               name="attendance_class"),
    path("attendance-report/principal/", views.AttendanceReportPrincipalView.as_view(), name="attendance-report-principal"),
    path("attendance-report/parent/", views.AttendanceReportParentView.as_view(), name="attendance-report-parent"),
    path('students/<int:student_id>/marks/', views.StudentMarksListView.as_view(), name='student-marks'),
    path('students/me/marks/', views.MyMarksListView.as_view(), name='my-marks'),
    path('standardsection/',views.StudentStandardView.as_view())

]
