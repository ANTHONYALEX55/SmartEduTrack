from django.urls import path
from .views import (AssignmentCreateView, AssignmentListView,
                AssignmentSubmissionView,AssignmentReviewView,AssignmentSubmissionListView,
                ParentAssignmentTrackerView)

urlpatterns = [
    path('upload/', AssignmentCreateView.as_view(), name='assignment-upload'),
    path('assignments/', AssignmentListView.as_view(), name='assignment-list'),
    path('submit/', AssignmentSubmissionView.as_view(), name='assignment-submit'),
    path('review/<int:pk>/', AssignmentReviewView.as_view(), name='assignment-review'),
    path('<int:assignment_id>/submissions/', AssignmentSubmissionListView.as_view(), name='assignment-submission-list'),
    path('parent-tracker/', ParentAssignmentTrackerView.as_view(), name='parent-assignment-tracker'),
]
