from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.author = request.user      
            post.save()                     
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You can’t edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You can’t delete this post.")
    return render(request, 'blog/delete_confirm.html', {'post': post})

@login_required
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

@login_required
def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/view_post.html', {'post': post})
