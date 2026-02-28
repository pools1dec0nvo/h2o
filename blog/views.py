import markdown
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from home.models import DEPT_COLORS
from .forms import PostForm
from .models import Post, PostDept


def post_list(request):
    posts = Post.objects.select_related("poster").prefetch_related("dept_entries").all()
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
        "dept_colors": DEPT_COLORS,
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
            for dept_key in form.cleaned_data.get("departments", []):
                PostDept.objects.get_or_create(post=post, dept=dept_key)
            return redirect("blog:post_list")
    else:
        form = PostForm()
    return render(request, "blog/post_create.html", {"form": form})
