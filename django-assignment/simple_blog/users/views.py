from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from .forms import ProfileForm
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'login.html'

# User registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

# View user profile
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    is_following = False
    if request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=user).exists():
        is_following = True
    return render(request, 'profile.html', {'profile': profile, 'user': request.user, 'is_following': is_following})

# Edit user profile
@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_form.html', {'form': form})

# Follow a user
@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

# Unfollow a user
@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)
