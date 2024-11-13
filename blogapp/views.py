from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from .encryption import rsa_encrypt, caesar_encrypt, rsa_decrypt, caesar_decrypt
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
import os

def login_existing(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_post')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def get_public_key():
    key_path = os.path.join(settings.BASE_DIR, "config", "public_key.pem")
    with open(key_path, "r") as f:
        return f.read()

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.author = request.user
            
            post.encryption_type = form.cleaned_data['encryption_type']
            content = form.cleaned_data['content']

            if post.encryption_type == 'RSA':
                public_key = get_public_key() 
                post.encrypted_content = rsa_encrypt(content, public_key)
            elif post.encryption_type == 'Caesar':
                post.encrypted_content = caesar_encrypt(content)
            
            post.content = "" 

            post.save()
            
            form.save_m2m()

            return redirect('post_list')
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()
    display_posts = []
    private_key = get_public_key()

    for post in posts:
        if post.author == request.user or request.user in post.authorized_users.all():
            if post.encryption_type == 'RSA':
                content = rsa_decrypt(post.encrypted_content, private_key)
            elif post.encryption_type == 'Caesar':
                content = caesar_decrypt(post.encrypted_content)
        else:
            content = post.encrypted_content

        display_posts.append({
            'title': post.title,
            'content': content,
            'author': post.author,
        })

    return render(request, 'post_list.html', {'posts': display_posts})