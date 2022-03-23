from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Group, Follow

User = get_user_model()


def group_posts(request, slug):
    """This view render group posts."""
    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(group.posts.all(), settings.PAGE_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def index(request):
    """This view render main page."""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGE_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def post_detail(request, post_id):
    """This view render post detail by its id."""
    post = get_object_or_404(Post, pk=post_id)
    count_of_posts = post.author.posts.count()
    comments = post.comments.all()
    form = CommentForm()
    context = {
        'page_obj': post,
        'count_of_posts': count_of_posts,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


def profile(request, username):
    """This view render profile page by its username."""
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user, author=author).exists()
    else:
        following = False
    post_list = author.posts.all()
    count_of_posts = post_list.count()
    paginator = Paginator(post_list, settings.PAGE_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'page_obj': page_obj,
        'author': author,
        'count_of_posts': count_of_posts,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_create(request):
    """This view create new post in database."""
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm(
        request.POST,
        files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=post.author.username)


@login_required
def post_edit(request, post_id):
    """This view edits the post by its id and saves changes in database."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method != 'POST':
        form = PostForm(instance=post)
        return render(request, 'posts/create_post.html', {'form': form,
                                                          'is_edit': True})
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, 'posts/create_post.html', {'form': form,
                                                      'is_edit': True})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Напишите view-функцию страницы, куда будут выведены посты авторов,
    на которых подписан текущий пользователь.
    """
    authors_id = request.user.follower.all().values_list('author', flat=True)
    posts = Post.objects.filter(author_id__in=authors_id)
    paginator = Paginator(posts, settings.PAGE_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {'page_obj': page_obj}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    Follow.objects.create(user=user, author=author)
    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=user, author=author).delete()
    return redirect('posts:follow_index')

