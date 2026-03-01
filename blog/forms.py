from django import forms

from core.models import Department
from .models import Post


class PostForm(forms.ModelForm):
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
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

    def clean_departments(self):
        depts = self.cleaned_data.get("departments", [])
        if len(depts) > 1:
            general_selected = any(d.is_general for d in depts)
            if general_selected:
                raise forms.ValidationError(
                    "General cannot be combined with other departments."
                )
        return depts
