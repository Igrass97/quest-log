from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Post

# /
def latests_posts(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]

    context = {
        'latest_post_list': latest_post_list,
    }
    return render(request, 'blog/index.html', context)

# /all
def all_posts(request):
    all_posts_list = Post.objects.order_by('-pub_date')

    context = {
        'all_posts_list': all_posts_list,
    }
    return render(request, 'blog/all_posts.html', context)

# /:id/post_detail
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {"post": post})

# /:id/comment
def comment(request, post_id):
    return HttpResponse("You're commenting in the post %s." % post_id)

# /:id/like
def like(request, post_id):
    return HttpResponse("You're liking the post %s." % post_id)