from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile



# ユーザー登録すると、自動でプロフィールが作成される
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)
    if created:
        Profile.objects.create(user=instance)




    
        
