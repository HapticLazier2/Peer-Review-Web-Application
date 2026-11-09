from django.urls import path

from core.views import assignments, auth

urlpatterns = [
    path("auth/csrf/", auth.csrf),
    path("auth/login/", auth.login_view),
    path("auth/logout/", auth.logout_view),
    path("auth/me/", auth.me),
    path("courses/", assignments.course_list),
    path("assignments/", assignments.assignment_list),
    path("assignments/<int:pk>/", assignments.assignment_detail),
]