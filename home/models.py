from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        SYS = "sys", "System"
        COLLAB = "collab", "Collaborator"
        NORMAL = "normal", "Normal"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.NORMAL)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    curriculum = models.FileField(upload_to="curricula/", blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    @property
    def is_sys(self):
        return self.role == self.Role.SYS

    @property
    def is_collab(self):
        return self.role == self.Role.COLLAB

    def save(self, *args, **kwargs):
        if self.role == self.Role.SYS:
            self.is_superuser = True
            self.is_staff = True
        elif self.role == self.Role.COLLAB:
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

    @property
    def leader_of(self):
        from core.models import Department
        return Department.objects.filter(
            dept_memberships__user=self,
            dept_memberships__role="leader",
        )

    @property
    def member_of(self):
        from core.models import Department
        return Department.objects.filter(
            dept_memberships__user=self,
            dept_memberships__role="member",
        )
