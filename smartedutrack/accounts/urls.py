from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [
    path('create-teacher-parent/', views.CreateTeacherParentView.as_view(), 
         name='create-teacher-parent'),
    path("login/", views.SessionLoginView.as_view(), name="session-login"),
    path("logout/", views.SessionLogoutView.as_view(), name="session-logout"),
    path("password-reset-request/", views.PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset-confirm/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
]