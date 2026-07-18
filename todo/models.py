from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    CATEGORY_CHOICES = [
        ("Study", "Study"),
        ("Work", "Work"),
        ("Personal", "Personal"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="Personal"
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    completed = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)

    attachment = models.FileField(
        upload_to="attachments/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title