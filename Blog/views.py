from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category, Profile
from django.shortcuts import render, redirect
from .forms import CommentForm, PostForm
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_post(request):

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(
        request,
        'blog/create_post.html',
        {'form': form}
    )


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(
        request,
        'blog/post_list.html',
        {'posts': posts}
    )

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()

    comments = post.comments.all()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'blog/post_detail.html', context)

def post_update(request, id):

    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('post_list')

    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/create_post.html',
        {'form': form}
    )

def delete_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(
        request,
        'blog/post_delete.html',
        {'post': post}
    )

def category_posts(request, category_id):
    category = Category.objects.get(id=category_id)

    posts = Post.objects.filter(
        category=category
    )

    return render(request,
        'blog/post_list.html',
        {'posts': posts}
    )

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
    user=request.user
)

    user_posts = Post.objects.filter(
        author=request.user
    )

    context = {
        'profile': profile,
        'user_posts': user_posts
    }

    return render(
        request,
        'blog/profile.html',
        context
    )

@login_required
def settings_page(request):

    return render(
        request,
        'blog/settings.html'
    )

@login_required
def my_posts(request):

    posts = Post.objects.filter(
        author=request.user
    )

    return render(
        request,
        'blog/my_posts.html',
        {'posts': posts}
    )

