from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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
 
        
@login_required        
def send_invitation(request):
    '''
    友達申請をする（sendする）
    '''
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')  # send状態の関係性を作る
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile')


@login_required
def invites_received_view(request):
    '''
    友達申請の受け取り
    '''
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)  # 友達申請をしてきたが、まだ承認していないユーザー
    results = list(map(lambda x: x.sender, qs))  # 送り主の情報だけ取得
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'qs': results,
        'is_empty': is_empty
    }
    return render(request, 'profiles/invites.html', context)


@login_required
def accept_invitation(request):
    '''
    友達申請を承認する
    '''
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:invites')

@login_required
def reject_invitation(request):
    '''
    友達申請を拒否する
    '''
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:invites')


@login_required
def remove_from_friends(request):
    '''
    友達を解除する
    '''
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()  # 一方的に友達解除する
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all_profiles')
    
            