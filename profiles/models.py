from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
# from .utils import get_random_code


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        '''
        友達申請するユーザー情報 (まだ友達ではないユーザー)
        '''
        profiles = Profile.objects.all().exclude(user=sender)  # senderは自分（request.user）
        profile = Profile.objects.get(user=sender)  # 自分（request.user）
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':  # 送るは、not acceptなのでどちらかがacceptだった場合、両者accepted.
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)
        
        available = [profile for profile in profiles if profile not in accepted]  # まだ友達ではないユーザー
        print(available)
        return available
    
    def get_all_profiles_without_me(self, me):
        '''
        自分以外のユーザー情報
        '''
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    '''
    プロフィールモデル
    '''
    first_name = models.CharField('姓', max_length=200, blank=True)
    last_name = models.CharField('名', max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="よろしくお願いします。", max_length=300)
    email = models.EmailField(max_length=200, blank=True)   
    avatar = models.ImageField(default='avatar.png', upload_to='avatars') 
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    objects = ProfileManager()
    
    def __str__(self):
        return self.user.username
    
    def get_friends(self):
        '''
        全ての友達
        '''
        return self.friends.all()
    
    def get_friends_count(self):
        '''
        友達の数
        '''
        return self.friends.all().count()
    
    def get_posts_count(self):
        '''
        投稿の数
        '''
        return self.posts.all().count()     

    def get_all_authors_posts(self):
        '''
        全ての投稿
        '''
        return self.posts.all()
    
    def get_likes_given_no(self):
        '''
        全ての投稿の与えたいいね数
        '''
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value=='Like':
                total_liked += 1
        return total_liked
    
    def get_likes_recieved_no(self):
        '''
        全ての投稿の受け取ったいいね数
        '''
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)
    

    
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class Relationship(models.Model):
    '''
    関係性モデル
    '''
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(choices=STATUS_CHOICES, max_length=8)   
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
    
    