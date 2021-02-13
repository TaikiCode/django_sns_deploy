from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile, Relationship
from .forms import ProfileModelForm


@login_required
def my_profile_view(request):
    '''
    自分のプロフィール情報
    '''
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'profiles/my_profile.html', context)


class ProfileListView(LoginRequiredMixin, ListView):
    '''
    自分以外のユーザーを一覧表示
    '''
    model = Profile
    template_name = 'profiles/profile_list.html'
    
    def get_queryset(self):
        '''
        自分以外の情報取得
        '''
        qs = Profile.objects.get_all_profiles_without_me(self.request.user)
        return qs  # object_list
    
    def get_context_data(self, **kwargs):
        '''
        友達申請したユーザー、友達申請してきたユーザー名を取得
        '''
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)  # 自分のプロフィール
        rel_r = Relationship.objects.filter(sender=profile)  # 申請した相手の情報
        rel_s = Relationship.objects.filter(receiver=profile)  # 申請してきた相手の情報
        rel_receiver = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)  # ユーザー名だけ取り出す
        rel_sender = []
        for item in rel_s:
            rel_sender.append(item.sender.user)
            
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        
        if len(self.get_queryset()) == 0:  # 自分以外ユーザーが存在しない場合
            context['is_empty'] = True
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    '''
    特定のユーザーの情報
    return (
        rel_receiver: 申請したユーザーのユーザー名
        rel_sender: 申請してきたユーザーのユーザー名
        posts: そのユーザーの全ての投稿 
        len_posts: そのユーザーの投稿があるかどうか（真偽値）
    )
    '''
    model = Profile
    template_name = 'profiles/profile_detail.html'
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)  # slugから特定のユーザーを取得
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        rel_sender = []
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context
        
        
        
        
        
        
