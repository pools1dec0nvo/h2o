from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm

from core.models import Department
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "autofocus": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True,
        widget=forms.TextInput(attrs={"placeholder": "First name"}))
    last_name = forms.CharField(max_length=150, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last name"}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    linkedin_url = forms.URLField(required=False,
        widget=forms.URLInput(attrs={"placeholder": "LinkedIn URL (optional)"}))
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "linkedin_url", "profile_photo", "password1", "password2")


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True,
        widget=forms.TextInput(attrs={"placeholder": "First name"}))
    last_name = forms.CharField(max_length=150, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last name"}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    linkedin_url = forms.URLField(required=False,
        widget=forms.URLInput(attrs={"placeholder": "https://linkedin.com/in/…"}))
    phone_number = forms.CharField(max_length=30, required=False,
        widget=forms.TextInput(attrs={"placeholder": "+351 900 000 000"}))
    profile_photo = forms.ImageField(required=False,
        widget=forms.FileInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "linkedin_url", "phone_number", "profile_photo")


class DeptOtherForm(forms.Form):
    """Lets a user pick their secondary (non-main) departments."""
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Other departments",
    )


class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"placeholder": "New password"}),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm new password"}),
    )
