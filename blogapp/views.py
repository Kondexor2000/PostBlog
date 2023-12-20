# views.py

from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # assuming user is logged in
            post.save()
            return redirect('post_list')  # change 'post_list' to the name of your post list view
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})