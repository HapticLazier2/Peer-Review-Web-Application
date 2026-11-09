from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ROLE_CHOICES = [(STUDENT, "Student"), (INSTRUCTOR, "Instructor")]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    @property
    def is_instructor(self):
        return self.role == self.INSTRUCTOR

class Course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses_taught"
    )
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="courses", blank=True)

    def __str__(self):
        return self.code

class Assignment(models.Model):
    CODE = "code"
    WRITTEN = "written"
    OTHER = "other"
    TYPE_CHOICES = [(CODE, "Code"), (WRITTEN, "Written response"), (OTHER, "Other")]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    submission_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=CODE)
    submission_due = models.DateTimeField()
    review_due = models.DateTimeField()
    reviewers_per_submission = models.PositiveSmallIntegerField(default=2)
    reviewers_assigned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submission_due"]

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions"
    )
    file = models.FileField(upload_to="submissions/")
    original_name = models.CharField(max_length=255)
    anon_id = models.CharField(max_length=8)
    protected_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("assignment", "author"), ("assignment", "anon_id")]

    def original_text(self):
        with self.file.open("rb") as f:
            return f.read().decode("utf-8").rstrip("\n")

class Review(models.Model):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    STATUS_CHOICES = [
        (NOT_STARTED, "Not started"),
        (IN_PROGRESS, "In progress"),
        (SUBMITTED, "Submitted"),
    ]

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_STARTED)
    submitted_at = models.DateTimeField(null=True, blank=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = [("submission", "reviewer")]
        ordering = ["id"]

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_line = models.PositiveIntegerField(null=True, blank=True)
    end_line = models.PositiveIntegerField(null=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]