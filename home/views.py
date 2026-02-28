from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from blog.models import Post
from .forms import ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm
from .models import User, DEPT_COLORS


def index(request):
    team = User.objects.filter(
        role__in=[User.Role.SYS, User.Role.COLLAB]
    ).prefetch_related("dept_other_entries").order_by("first_name")
    recent_posts = Post.objects.select_related("poster").order_by("-created_at")[:3]
    return render(request, "home/index.html", {
        "team": team,
        "recent_posts": recent_posts,
        "dept_colors": DEPT_COLORS,
    })


class UserLoginView(LoginView):
    template_name = "home/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


def user_logout(request):
    logout(request)
    return redirect("/")


@login_required
def edit_profile(request):
    profile_form = EditProfileForm(instance=request.user)
    password_form = ChangePasswordForm(user=request.user)
    profile_saved = False
    password_saved = False

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                # Only update photo if a new one was submitted
                if not request.FILES.get("profile_photo"):
                    profile_form.cleaned_data.pop("profile_photo", None)
                    profile_form.instance.profile_photo = request.user.profile_photo
                profile_form.save()
                profile_saved = True
        elif "save_password" in request.POST:
            password_form = ChangePasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                password_saved = True

    return render(request, "home/profile.html", {
        "profile_form": profile_form,
        "password_form": password_form,
        "profile_saved": profile_saved,
        "password_saved": password_saved,
    })


@login_required
def register(request):
    if not request.user.is_sys:
        raise PermissionDenied
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "home/register.html", {"form": form})
