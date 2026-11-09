from django.urls import path
from core import views

urlpatterns = [
    path("auth/me/", views.me),
]