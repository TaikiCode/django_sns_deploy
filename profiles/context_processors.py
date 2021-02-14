from .models import Profile, Relationship



def invitations_received_count(request):
    '''
    友達申請の数
    '''
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        count = Relationship.objects.invitations_received(profile_obj).count()
        return {'invites_count': count}
    return {}
    
