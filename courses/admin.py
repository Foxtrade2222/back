from django.contrib import admin

from courses.models import (
    Category,
    Course,
    CourseApprove,
    Module,
    Payment,
    Quiz,
    SeenTopic,
    Topic,
)

# Register your models here.
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Module)
admin.site.register(Quiz)
admin.site.register(CourseApprove)
admin.site.register(Payment)
admin.site.register(SeenTopic)
