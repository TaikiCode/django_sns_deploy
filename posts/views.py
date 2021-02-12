from django.shortcuts import render

from .models import Post, Like
from .forms import PostModelForm, CommentModelForm
from profiles.models import Profile




def post_comment_create_and_list_view(request):
    '''
    新規投稿、コメント投稿、一覧表示
    '''
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    # 初期設定
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    
    if 'submit_p_form' in request.POST:
        print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile  # 投稿者
            instance.save()
            p_form = PostModelForm()  # 更新
            post_added = True
            
    if 'submit_c_form' in request.POST:
        print(request.POST)
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()
            
    context = {
        'posts': posts,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added
    }
    return render(request, 'posts/home.html', context)
            

