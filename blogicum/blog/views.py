from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, User, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from django.views import View
from blog.forms import UserEditForm, CommentForm, PostForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required


# Create your views here.


def index_posts(posts):
    posts = posts.order_by('-pub_date')
    posts = posts.annotate(
        comment_count=Count("comment")
    ).order_by(
        "-pub_date"
    )
    return posts


def index(request):
    dt_now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=dt_now,
        is_published=True,
        category__is_published=True
    )
    posts = index_posts(posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def create_edit(request, post_id=None):
    dt_now = timezone.now()
    post = get_object_or_404(
        Post,
        pk=post_id,
        pub_date__lte=dt_now,
        is_published=True,
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def post_detail(request, post_id):
    dt_now = timezone.now()

    post = get_object_or_404(
        Post,
        pk=post_id,
    )

    if request.user != post.author:
        post = get_object_or_404(
            Post,
            pk=post_id,
            pub_date__lte=dt_now,
            is_published=True,
            category__is_published=True
        )
    comment_form = CommentForm()
    comments = Comment.objects.filter(post=post).order_by('created_at')
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'form': comment_form,
            'comments': comments
        }
    )


def add_comment(request, post_id):
    comm = request.POST['text']
    user = get_object_or_404(User, username=request.user)
    post = get_object_or_404(Post, pk=post_id)
    print(post.text)
    comm = Comment.objects.create(author=user, text=comm, post=post)
    if CommentForm(request.GET or None).is_valid():
        comm.save()
    return redirect('blog:post_detail', post_id)


def edit_comment(request, post_id, comment_id):
    comm = get_object_or_404(Comment, pk=comment_id, post__pk=post_id)
    form = CommentForm(request.POST or None, instance=comm)
    if form.is_valid():
        if request.user.pk == comm.author.pk:
            form.save()
        return redirect('blog:post_detail', post_id)
    return render(
        request,
        'blog/comment.html',
        {
            'form': form, 'comment': comm
        }
    )


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        pk=comment_id
    )
    if request.method == 'POST':
        if request.user.pk == comment.author.pk:
            comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    else:
        context = {
            "comment": comment
        }
        return render(request, "blog/comment.html", context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    dt_now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=dt_now,
        is_published=True,
        category=category
    )
    posts = index_posts(posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/category.html',
        {
            'page_obj': page_obj,
            'category': category
        }
    )


class Profile(View):
    template = 'blog/profile.html'

    def get(self, request, **kwargs):
        username = kwargs['username']
        profile = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=profile)
        posts = index_posts(posts)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        contex = {
            "profile": profile,
            'page_obj': page_obj
        }
        return render(request, self.template, contex)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
        context = {
            "form": form
        }
        return render(request, 'blog/user.html', context)
    form = UserEditForm(instance=request.user)
    context = {
        "form": form
    }
    return render(request, 'blog/user.html', context)


@login_required
def post_edit(request, post_id=None):
    form = PostForm()
    if request.method == 'POST':
        if post_id is not None:
            user = request.user
            user = get_object_or_404(User, username=user)
            form = PostForm(request.POST, request.FILES)
            instance = get_object_or_404(Post, pk=post_id)
            if user.pk != instance.author.pk:
                return redirect("blog:post_detail", post_id=post_id)
            if form.is_valid():
                post = get_object_or_404(
                    Post,
                    pk=post_id
                )
                post.text = form.cleaned_data["text"]
                post.title = form.cleaned_data["title"]
                post.pub_date = form.cleaned_data["pub_date"]
                post.category = form.cleaned_data["category"]
                post.location = form.cleaned_data["location"]
                post.save()
                return redirect("blog:post_detail", post_id=post_id)
        else:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect("blog:profile", username=post.author.username)
    else:
        if post_id is not None:
            instance = get_object_or_404(Post, pk=post_id)
            form = PostForm(instance=instance)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    context = {'form': form}
    if request.method == 'POST' and instance.author == request.user:
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)
