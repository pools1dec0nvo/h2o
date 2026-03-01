import markdown
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe

from core.models import Department
from .forms import PostForm
from .models import Post, PostDept


def post_list(request):
    posts = Post.objects.select_related("poster").prefetch_related("dept_entries__dept")

    dept_slug = request.GET.get("dept", "")
    year = request.GET.get("year", "")

    if dept_slug:
        posts = posts.filter(dept_entries__dept__slug=dept_slug)
    if year:
        try:
            posts = posts.filter(created_at__year=int(year))
        except ValueError:
            pass

    posts = posts.distinct()

    rendered = [
        {
            "post": post,
            "html_content": mark_safe(markdown.markdown(
                post.content,
                extensions=["extra", "codehilite", "toc"],
            )),
        }
        for post in posts
    ]

    return render(request, "blog/post_list.html", {
        "rendered_posts": rendered,
        "all_depts": Department.objects.all(),
        "years": Post.objects.dates("created_at", "year", order="DESC"),
        "active_dept": dept_slug,
        "active_year": year,
    })


@login_required
def post_create(request):
    if not (request.user.is_collab or request.user.is_sys):
        raise PermissionDenied
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.poster = request.user
            post.save()
            for dept in form.cleaned_data.get("departments", []):
                PostDept.objects.get_or_create(post=post, dept=dept)
            return redirect("blog:post_list")
    else:
        form = PostForm()
    return render(request, "blog/post_create.html", {"form": form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not (request.user.is_sys or (request.user.is_collab and post.poster == request.user)):
        raise PermissionDenied
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            post.dept_entries.all().delete()
            for dept in form.cleaned_data.get("departments", []):
                PostDept.objects.get_or_create(post=post, dept=dept)
            return redirect("blog:post_list")
    else:
        existing_depts = list(post.dept_entries.values_list("dept", flat=True))
        form = PostForm(instance=post, initial={"departments": existing_depts})
    return render(request, "blog/post_create.html", {"form": form, "editing": True, "post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not (request.user.is_sys or (request.user.is_collab and post.poster == request.user)):
        raise PermissionDenied
    if request.method == "POST":
        post.delete()
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
