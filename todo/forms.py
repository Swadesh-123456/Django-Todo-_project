from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "status",
            "completed",
            "due_date",
            "attachment",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Task Title"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Task Description"
            }),

            # ✅ CHANGE THIS
            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Category"
            }),

            "priority": forms.Select(attrs={
                "class": "form-select"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "completed": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "attachment": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }