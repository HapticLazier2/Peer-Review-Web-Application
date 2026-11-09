"""Auth Controller: login, logout, current user."""
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

GENERIC_ERROR = "Invalid username or password."
LOCKED_ERROR = "Too many failed attempts. Your account is locked for 15 minutes."


def _keys(username):
    u = (username or "").strip().lower()
    return f"login-fail:{u}", f"login-lock:{u}"


def user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "name": user.get_full_name() or user.username,
        "role": user.role,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf(request):
    """Sets the CSRF cookie the front end must send back on every change."""
    return Response({"ok": True})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    fail_key, lock_key = _keys(username)

    if cache.get(lock_key):
        return Response({"detail": LOCKED_ERROR}, status=403)

    user = authenticate(request, username=username, password=password)
    if user is None:
        failures = cache.get(fail_key, 0) + 1
        if failures >= settings.LOGIN_MAX_ATTEMPTS:
            cache.set(lock_key, True, settings.LOGIN_LOCKOUT_SECONDS)
            cache.delete(fail_key)
            return Response({"detail": LOCKED_ERROR}, status=403)
        cache.set(fail_key, failures, settings.LOGIN_LOCKOUT_SECONDS)
        return Response(
            {"detail": GENERIC_ERROR, "attempts_left": settings.LOGIN_MAX_ATTEMPTS - failures},
            status=400,
        )

    cache.delete(fail_key)
    login(request, user)
    return Response(user_payload(user))


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"ok": True})


@api_view(["GET"])
@permission_classes([AllowAny])
def me(request):
    if not request.user.is_authenticated:
        return Response(None)
    return Response(user_payload(request.user))