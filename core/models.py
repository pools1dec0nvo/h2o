from django.conf import settings
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


class SubTeam(models.Model):
    slug = models.SlugField(max_length=20, unique=True)
    name = models.CharField(max_length=30)
    portuguese_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default="#64748b")
    dept = models.ForeignKey(
        "core.Department",
        on_delete=models.CASCADE,
        related_name="sub_teams",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Sub-team"
        verbose_name_plural = "Sub-teams"

    def __str__(self):
        return self.name


class DeptMembership(models.Model):
    class Role(models.TextChoices):
        LEADER = "leader", "Team Leader"
        MEMBER = "member", "Member"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dept_memberships",
    )
    dept = models.ForeignKey(
        "core.Department",
        on_delete=models.CASCADE,
        related_name="dept_memberships",
    )
    role = models.CharField(max_length=10, choices=Role.choices)

    class Meta:
        ordering = ["role"]
        constraints = [
            models.UniqueConstraint(fields=["user", "dept"], name="uniq_user_dept")
        ]
        verbose_name = "Department Membership"
        verbose_name_plural = "Department Memberships"

    def __str__(self):
        return f"{self.user} - {self.dept} ({self.role})"
