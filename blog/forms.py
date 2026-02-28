from django import forms
from .models import Post, DEPT_CHOICES


class PostForm(forms.ModelForm):
    departments = forms.MultipleChoiceField(
        choices=DEPT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "post-form__dept-checks"}),
        label="Departments",
    )

    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={
                "placeholder": "Write your post in Markdown...",
                "rows": 20,
                "class": "post-form__source",
            }),
        }
        labels = {
            "content": "Content (Markdown)",
        }
