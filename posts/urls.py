from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.post_comment_create_and_list_view, name='home'),
    path('<pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('<pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('like/', views.like_post, name='like-post'),
]


    
