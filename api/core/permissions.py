"""Permission & Role Checks component.

Role checks happen on the server, so hiding a button in the UI is never the only protection.
"""
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    message = "Only instructors can do this."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_instructor)


def is_course_instructor(user, course):
    return user.is_instructor and course.instructor_id == user.id


def require_enrolled(user, course):
    if not course.students.filter(pk=user.pk).exists():
        raise PermissionDenied("You are not enrolled in this class.")


def require_can_view_submission(user, submission):
    """Author, an assigned reviewer, or the course instructor. Everyone else gets 403."""
    if submission.author_id == user.id:
        return
    if is_course_instructor(user, submission.assignment.course):
        return
    if submission.reviews.filter(reviewer=user).exists():
        return
    raise PermissionDenied("You do not have access to this submission.")


def require_can_view_review(user, review):
    if review.reviewer_id == user.id:
        return
    if review.submission.author_id == user.id and review.status == review.SUBMITTED:
        return
    if is_course_instructor(user, review.submission.assignment.course):
        return
    raise PermissionDenied("You do not have access to this review.")