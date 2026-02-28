from django.contrib.auth.models import AbstractUser
from django.db import models


DEPT_NAMES = {
    "elec": "Electronics",
    "dev": "Software Engineering",
    "math": "Statistics",
    "finance": "Finance",
    "relations": "External Relations",
}

DEPT_COLORS = {
    "elec": "#e53e3e",
    "dev": "#f6c90e",
    "math": "#38a169",
    "finance": "#3182ce",
    "relations": "#d53f8c",
}


class User(AbstractUser):
    class Role(models.TextChoices):
        SYS = "sys", "System"
        COLLAB = "collab", "Collaborator"
        NORMAL = "normal", "Normal"

    class Dept(models.TextChoices):
        ELEC = "elec", DEPT_NAMES["elec"]
        DEV = "dev", DEPT_NAMES["dev"]
        MATH = "math", DEPT_NAMES["math"]
        FINANCE = "finance", DEPT_NAMES["finance"]
        RELATIONS = "relations", DEPT_NAMES["relations"]

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.NORMAL)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    linkedin_url = models.URLField(blank=True)

    dept_main = models.CharField(
        max_length=20,
        choices=Dept.choices,
        blank=True,
        verbose_name="Main Department",
    )

    @property
    def is_sys(self):
        return self.role == self.Role.SYS

    @property
    def is_collab(self):
        return self.role == self.Role.COLLAB

    def get_dept_main_color(self):
        return DEPT_COLORS.get(self.dept_main, "#64748b")

    def save(self, *args, **kwargs):
        if self.is_sys:
            self.is_staff = True
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        if self.is_sys:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_sys:
            return True
        return super().has_module_perms(app_label)


class UserDeptOther(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dept_other_entries",
    )
    dept = models.CharField(max_length=20, choices=User.Dept.choices)

    class Meta:
        unique_together = ("user", "dept")

    def get_dept_color(self):
        return DEPT_COLORS.get(self.dept, "#64748b")

    def get_dept_display(self):
        return DEPT_NAMES.get(self.dept, self.dept)
