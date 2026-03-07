from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from blog.models import Post
from core.models import Department, DeptMembership
from .forms import ChangePasswordForm, MemberDeptForm, EditProfileForm, LoginForm, RegisterForm
from .models import User


def index(request):
    team = (
        User.objects.filter(role__in=[User.Role.SYS, User.Role.COLLAB])
        .prefetch_related("dept_memberships__dept")
        .order_by("first_name")
    )
    recent_posts = Post.objects.select_related("poster").order_by("-created_at")[:3]

    depts = []
    for dept in Department.objects.prefetch_related("sub_teams").exclude(slug="general"):
        leaders = [
            u for u in team
            if any(
                m.dept_id == dept.pk and m.role == DeptMembership.Role.LEADER
                for m in u.dept_memberships.all()
            )
        ]
        members = [
            u for u in team
            if any(
                m.dept_id == dept.pk and m.role == DeptMembership.Role.MEMBER
                for m in u.dept_memberships.all()
            )
        ]
        sub_teams = [
            {"name": st.name, "description": st.description, "color": st.color}
            for st in dept.sub_teams.all()
        ]
        depts.append({
            "key": dept.slug,
            "name": dept.full_name,
            "color": dept.color,
            "description": dept.description,
            "icon_svg": dept.icon_svg,
            "leaders": leaders,
            "members": members,
            "sub_teams": sub_teams,
        })

    depts_simple = [d for d in depts if len(d["sub_teams"]) <= 1]
    depts_complex = [d for d in depts if len(d["sub_teams"]) > 1]

    return render(request, "home/index.html", {
        "team": team,
        "recent_posts": recent_posts,
        "depts": depts,
        "depts_simple": depts_simple,
        "depts_complex": depts_complex,
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
    current_member_depts = list(
        DeptMembership.objects.filter(
            user=request.user,
            role=DeptMembership.Role.MEMBER,
        ).values_list("dept", flat=True)
    )
    profile_form = EditProfileForm(instance=request.user)
    password_form = ChangePasswordForm(user=request.user)
    dept_form = MemberDeptForm(initial={"departments": current_member_depts})
    profile_saved = False
    password_saved = False
    dept_saved = False

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                text_fields = ["first_name", "last_name", "email", "linkedin_url", "phone_number"]
                has_photo = bool(request.FILES.get("profile_photo"))
                has_cv = bool(request.FILES.get("curriculum"))
                extra = (["profile_photo"] if has_photo else []) + (["curriculum"] if has_cv else [])
                if extra:
                    instance = profile_form.save(commit=False)
                    instance.save(update_fields=text_fields + extra)
                else:
                    instance = profile_form.save(commit=False)
                    instance.save(update_fields=text_fields)
                profile_saved = True
        elif "save_password" in request.POST:
            password_form = ChangePasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                password_saved = True
        elif "save_depts" in request.POST:
            dept_form = MemberDeptForm(request.POST)
            if dept_form.is_valid():
                selected = set(dept_form.cleaned_data["departments"])
                DeptMembership.objects.filter(
                    user=request.user,
                    role=DeptMembership.Role.MEMBER,
                ).exclude(dept__in=selected).delete()
                for dept in selected:
                    DeptMembership.objects.get_or_create(
                        user=request.user,
                        dept=dept,
                        defaults={"role": DeptMembership.Role.MEMBER},
                    )
                dept_saved = True

    return render(request, "home/profile.html", {
        "profile_form": profile_form,
        "password_form": password_form,
        "dept_form": dept_form,
        "profile_saved": profile_saved,
        "password_saved": password_saved,
        "dept_saved": dept_saved,
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
