from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='all_posts'),
    path('<int:pk>/detail', views.DetailView.as_view(), name='post_detail'),
    path('<int:pk>/comment', views.comment, name='comment'),
    path('<int:pk>/like', views.like, name='like'),
]