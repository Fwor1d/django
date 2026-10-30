from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProfileUpdateForm, SignUpForm, UserUpdateForm
from .models import Profile

User = get_user_model()


def signup(request):
    if request.user.is_authenticated:
        return redirect("blog:post_list")
    form = SignUpForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("blog:post_list")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile_view(request, username=None):
    profile_user = (get_object_or_404(User, username=username)
                    if username else request.user)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    return render(request, "accounts/profile.html", {
        "profile_user": profile_user, "profile": profile,
    })


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    u_form = UserUpdateForm(request.POST if request.method == "POST" else None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST if request.method == "POST" else None, request.FILES if request.method == "POST" else None, instance=profile)
    if request.method == "POST" and u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        return redirect("profile")
    return render(request, "accounts/profile_edit.html", {
        "u_form": u_form, "p_form": p_form,
    })
