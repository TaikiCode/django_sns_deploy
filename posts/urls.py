from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.post_comment_create_and_list_view, name='home'),
]
