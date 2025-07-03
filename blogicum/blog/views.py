from django.shortcuts import get_object_or_404, render
from django.db.models.functions import Now
from .models import Category, Post


def index(request):
    posts = (
        Post.objects
        .select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            pub_date__lte=Now(),
            category__is_published=True,
        )
        .order_by('-pub_date')[:5]
    )
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = (
        category.posts
        .select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            pub_date__lte=Now(),
        )
        .order_by('-pub_date')
    )
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        pk=id,
        is_published=True,
        pub_date__lte=Now(),
        category__is_published=True,
    )
    return render(request, 'blog/detail.html', {'post': post})
