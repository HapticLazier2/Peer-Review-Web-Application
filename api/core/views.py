from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def me(request):
    u = request.user
    return Response({"id": u.id, "username": u.username, "role": u.role})