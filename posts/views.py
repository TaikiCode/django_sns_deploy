from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Like
from .forms import PostModelForm, CommentModelForm
from profiles.models import Profile


@login_required
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
            

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:home')
    
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        # 投稿者本人しか編集できないようにする
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, '権限がありません。')
            return super().form_valid(form)
    

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:home')
    
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        # 投稿者本人しか編集できないようにする
        if not obj.author.user == self.request.user:
            messages.warning(self.request, '権限がありません。')
        return obj
    

@login_required
def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        
        # 一度しかlikeできない、2回目は解除
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
            
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        '''
        like：オブジェクト
        created：真偽値（getの場合false、createの場合true）
        '''
        
        # すでにオブジェクトが存在する場合
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        # 初めてLikeする場合
        else:
            like.value = 'Like'      
            post_obj.save() 
            like.save() 
        
        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }    
        return JsonResponse(data, safe=False)
    return redirect('posts:home')
         
                
       
       
                    
       
           
            
     
        
                    
  
                
            
            
