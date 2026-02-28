from django.conf import settings
from django.db import models

from home.models import DEPT_NAMES, DEPT_COLORS


DEPT_CHOICES = [(k, v) for k, v in DEPT_NAMES.items()]


class Post(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    content = models.TextField(help_text="Write in Markdown.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PostDept(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="dept_entries")
    dept = models.CharField(max_length=20, choices=DEPT_CHOICES)

    class Meta:
        unique_together = ("post", "dept")

    def get_dept_color(self):
        return DEPT_COLORS.get(self.dept, "#64748b")

    def get_dept_display_name(self):
        return DEPT_NAMES.get(self.dept, self.dept)
