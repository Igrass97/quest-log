from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.latests_posts, name='latests_posts'),
    path('all', views.all_posts, name='all_posts'),
    path('<int:post_id>/detail', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment', views.comment, name='comment'),
    path('<int:post_id>/like', views.like, name='like'),
]