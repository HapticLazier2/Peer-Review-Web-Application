from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User


@admin.register(User)
class PeerProofUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("PeerProof", {"fields": ("role",)}),)
    list_display = ("username", "first_name", "last_name", "role")