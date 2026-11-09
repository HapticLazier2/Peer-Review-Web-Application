from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Assignment, Comment, Course, Review, Submission, User


@admin.register(User)
class PeerProofUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("PeerProof", {"fields": ("role",)}),)
    list_display = ("username", "first_name", "last_name", "role")


admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Review)
admin.site.register(Comment)