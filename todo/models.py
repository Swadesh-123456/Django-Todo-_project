from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    category = models.CharField(max_length=50)

    priority = models.CharField(
        max_length=10,
        choices=[
            ('High', 'High'),
            ('Medium', 'Medium'),
            ('Low', 'Low'),
        ],
        default='Medium'
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Todo', 'Todo'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
        ],
        default='Todo'
    )

    due_date = models.DateField(null=True, blank=True)

    attachment = models.FileField(
        upload_to='attachments/',
        blank=True,
        null=True
    )

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title