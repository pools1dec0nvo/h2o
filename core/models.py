from django.db import models


class Department(models.Model):
    slug = models.SlugField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    portuguese_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default="#64748b")
    is_general = models.BooleanField(
        default=False,
        help_text="If set, this dept cannot be combined with others on a post.",
    )

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.full_name
