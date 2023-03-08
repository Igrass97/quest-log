from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone

from .models import Post
from django import forms

DETAIL_TEMPLATE = 'blog/post_detail.html'
INDEX_TEMPLATE = 'blog/index.html'

class IndexView(ListView):
    model = Post
    template_name = INDEX_TEMPLATE

    # Replace the queryset (post_list) with a custom one
    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

# /:pk/detail
class DetailView(DetailView):
    model = Post
    template_name = DETAIL_TEMPLATE

    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        """
        Add the like count to the context.
        """
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

class PostCreateView(CreateView):
    model = Post
    fields = ['post_text']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:all_posts')

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        """
        form.instance.pub_date = timezone.now()  # set pub_date to current date/time
        return super().form_valid(form)
