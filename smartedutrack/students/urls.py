from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name="student-register"),
      path('link-parent/', views.LinkParentToStudentView.as_view(), name="link-parent-student"),
]
