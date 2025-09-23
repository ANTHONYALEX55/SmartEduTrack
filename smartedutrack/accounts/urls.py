from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('create-teacher-parent/', views.CreateTeacherParentView.as_view(), 
         name='create-teacher-parent'),
    path("login/", csrf_exempt(views.SessionLoginView.as_view()), name="session-login"),
    path("logout/", views.SessionLogoutView.as_view(), name="session-logout"),
    path("password-reset-request/", views.PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset-confirm/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]