from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Post

DETAIL_TEMPLATE = 'blog/post_detail.html'
INDEX_TEMPLATE = 'blog/index.html'

class IndexView(generic.ListView):
    model = Post
    template_name = INDEX_TEMPLATE

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')[:5]

# /:pk/detail
class DetailView(generic.DetailView):
    model = Post
    template_name = DETAIL_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['like_count'] = context['post'].like_set.count()
        return context

# /:pk/comment
def comment(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        comment_text = request.POST['comment_text']
        if not comment_text:
            return render(request, DETAIL_TEMPLATE, {"post": post, "error": "Comment cannot be empty"})
    except (Post.DoesNotExist):
        return HttpResponse("Post does not exist")
    except (KeyError):
        return render(request, DETAIL_TEMPLATE, {"post": post, "error": "Comment cannot be empty"})
    else:
        post.comment_set.create(comment_text=request.POST['comment_text'])
        post.save()
        return HttpResponseRedirect(reverse('blog:post_detail', args=[pk]))

# /:pk/like
def like(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
    except (Post.DoesNotExist):
        return HttpResponse("Post does not exist")
    else:
        post.like_set.create()
        post.save()
        return HttpResponseRedirect(reverse('blog:post_detail', args=[pk]))

