from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# from .utils import get_random_code



class Profile(models.Model):
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)
    


