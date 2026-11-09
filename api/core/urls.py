from django.urls import path

from core.views import auth

urlpatterns = [
    path("auth/csrf/", auth.csrf),
    path("auth/login/", auth.login_view),
    path("auth/logout/", auth.logout_view),
    path("auth/me/", auth.me),
]