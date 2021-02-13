from django.urls import path
from . import views


app_name = 'profiles'



urlpatterns = [
    path('my-profile/', views.my_profile_view, name='my-profile'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all_profiles'),
    path('profile/<slug>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('invites/', views.invites_received_view, name='invites'),
    path('invites/accept/', views.accept_invitation, name='accept-invite'),
    path('invites/reject/', views.reject_invitation, name='reject-invite'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend')
]

