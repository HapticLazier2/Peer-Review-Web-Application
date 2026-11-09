"""Assignment Controller: list and create assignments."""
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from core.models import Assignment, Course, Review
from core.permissions import IsInstructor, is_course_instructor


class AssignmentCreateSerializer(serializers.ModelSerializer):
    reviewers_per_submission = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Assignment
        fields = [
            "course", "title", "instructions", "submission_type",
            "submission_due", "review_due", "reviewers_per_submission",
        ]

    def validate(self, data):
        if data["review_due"] <= data["submission_due"]:
            raise serializers.ValidationError(
                "The review due date must be after the submission due date."
            )
        return data


def assignment_payload(a):
    return {
        "id": a.id,
        "title": a.title,
        "instructions": a.instructions,
        "submission_type": a.submission_type,
        "course": a.course.code,
        "submission_due": a.submission_due,
        "review_due": a.review_due,
        "reviewers_per_submission": a.reviewers_per_submission,
        "is_open": a.submission_due > timezone.now(),
    }


@api_view(["GET", "POST"])
def assignment_list(request):
    user = request.user

    if request.method == "POST":
        if not user.is_instructor:
            raise PermissionDenied("Only instructors can create assignments.")
        ser = AssignmentCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        if not is_course_instructor(user, ser.validated_data["course"]):
            raise PermissionDenied("You do not teach this class.")
        a = ser.save()
        return Response(assignment_payload(a), status=201)

    if user.is_instructor:
        assignments = Assignment.objects.filter(course__instructor=user).select_related("course")
        data = []
        for a in assignments:
            p = assignment_payload(a)
            reviews = Review.objects.filter(submission__assignment=a)
            p["submission_count"] = a.submissions.count()
            p["reviews_total"] = reviews.count()
            p["reviews_submitted"] = reviews.filter(status=Review.SUBMITTED).count()
            data.append(p)
        return Response(data)

    # Students only see assignments for classes they are enrolled in.
    assignments = Assignment.objects.filter(course__students=user).select_related("course")
    data = []
    for a in assignments:
        p = assignment_payload(a)
        sub = a.submissions.filter(author=user).first()
        p["submission_id"] = sub.id if sub else None
        p["feedback_count"] = sub.reviews.filter(status=Review.SUBMITTED).count() if sub else 0
        data.append(p)
    return Response(data)


@api_view(["GET"])
def assignment_detail(request, pk):
    a = get_object_or_404(Assignment.objects.select_related("course"), pk=pk)
    user = request.user
    if not (is_course_instructor(user, a.course) or a.course.students.filter(pk=user.pk).exists()):
        raise PermissionDenied("You do not have access to this assignment.")
    return Response(assignment_payload(a))


@api_view(["GET"])
@permission_classes([IsInstructor])
def course_list(request):
    courses = Course.objects.filter(instructor=request.user)
    return Response([{"id": c.id, "code": c.code, "name": c.name} for c in courses])