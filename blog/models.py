from django.conf import settings
from django.db import models


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
    dept = models.ForeignKey(
        "core.Department",
        on_delete=models.CASCADE,
        related_name="post_entries",
    )

    class Meta:
        unique_together = ("post", "dept")
