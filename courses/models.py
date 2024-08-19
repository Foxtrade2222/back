from django.conf import settings
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField()
    price = models.FloatField(default=0)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="my_courses", on_delete=models.CASCADE
    )
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="courses")
    category = models.ForeignKey(
        Category,
        related_name="courses",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    path_preview_image = models.URLField(max_length=500, default="Sin imagen")
    is_active = models.BooleanField(default=False)
    views = models.PositiveBigIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.title}"

    @property
    def modules(self):
        return self.modules


class Module(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        related_name="modules",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="Sin asignar")
    files = models.JSONField(blank=True, null=True)
    links = models.JSONField(blank=True, null=True)
    seen = models.BooleanField(default=False)
    video = models.CharField(max_length=500, default="Sin imagen")

    module = models.ForeignKey(
        Module,
        related_name="topics",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    course = models.OneToOneField(
        Course,
        related_name="quizzes",
        on_delete=models.CASCADE,
    )
    questions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course}"


class CourseApprove(models.Model):
    course_id = models.CharField(max_length=10)
    student_id = models.CharField(max_length=10)
    certificate_url = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_id}-{self.student_id}"


class Payment(models.Model):
    email = models.CharField(max_length=50)
    body = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email


class SeenTopic(models.Model):
    # topic_id = models.CharField(max_length=10)
    topic = models.ForeignKey(
        Topic,
        related_name="seens",
        on_delete=models.CASCADE,
    )
    student_id = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.topic)

    class Meta:
        ordering = ("-created_at",)
