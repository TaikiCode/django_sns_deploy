from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Relationship



# ユーザー登録すると、自動でプロフィールが作成される
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)
    if created:
        Profile.objects.create(user=instance)
        

# statusをacceptedにすると、自動でfriendsに追加する
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    if instance.status == 'accepted':  # 一方がacceptすれば、どちらもfriendになる
        sender.friends.add(receiver.user)
        receiver.friends.add(sender.user)
        sender.save()
        receiver.save()
    

# Relationshipの関係が削除されたら、自動でfriendsも削除する（正確には削除される前）
@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()



    
        


