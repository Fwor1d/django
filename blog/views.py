from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import urlencode

from .forms import CommentForm, PostForm
from .models import Post


def home(request):
    posts = Post.objects.filter(is_published=True).select_related("author")[:3]
    return render(request, "blog/home.html", {"latest_posts": posts})


def about(request):
    return render(request, "blog/about.html")


def post_list(request):
    query = request.GET.get("q", "").strip()
    posts = (Post.objects.filter(is_published=True)
             .select_related("author")
             .annotate(comment_count=Count("comments")))
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query) |
                             Q(summary__icontains=query))
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {
        "posts": page_obj,
        "page_obj": page_obj,
        "query": query,
        "query_parameter": "&" + urlencode({"q": query}) if query else "",
    })


def get_visible_post(request, **criteria):
    post = get_object_or_404(Post.objects.select_related("author"), **criteria)
    if not post.is_published and not (request.user.is_authenticated and
                                       (request.user.is_staff or post.author_id == request.user.pk)):
        raise Http404("Публикация не найдена")
    return post


def legacy_post_detail(request, pk):
    post = get_visible_post(request, pk=pk)
    return redirect(post.get_absolute_url(), permanent=True)


def post_detail(request, year, month, day, slug):
    post = get_visible_post(request, slug=slug, created_at__year=year,
                            created_at__month=month, created_at__day=day)
    comments = post.comments.select_related("author")
    if request.method == "POST":
        if not request.user.is_authenticated:
            login_url = reverse("login")
            return redirect(f"{login_url}?{urlencode({'next': request.path})}")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url() + "#comments")
    else:
        form = CommentForm()
    return render(request, "blog/post_detail.html", {
        "post": post, "comments": comments, "form": form,
        "canonical_url": request.build_absolute_uri(post.get_absolute_url()),
    })


@login_required
def post_create(request):
    form = PostForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post.get_absolute_url())
    return render(request, "blog/post_form.html", {"form": form, "editing": False})


def _get_editable_post(request, **criteria):
    post = get_object_or_404(Post, **criteria)
    if post.author_id != request.user.pk and not request.user.is_superuser:
        raise PermissionDenied("Редактировать публикацию может только автор.")
    return post


@login_required
def post_edit(request, year, month, day, slug):
    post = _get_editable_post(request, slug=slug, created_at__year=year,
                              created_at__month=month, created_at__day=day)
    form = PostForm(request.POST if request.method == "POST" else None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(post.get_absolute_url())
    return render(request, "blog/post_form.html", {"form": form, "editing": True, "post": post})


@login_required
def post_delete(request, year, month, day, slug):
    post = _get_editable_post(request, slug=slug, created_at__year=year,
                              created_at__month=month, created_at__day=day)
    if request.method == "POST":
        post.delete()
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
