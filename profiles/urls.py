from django.urls import path
from . import views


app_name = 'profiles'



urlpatterns = [
    path('my-profile/', views.my_profile_view, name='my-profile'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all_profiles'),
    path('profile/<slug>/', views.ProfileDetailView.as_view(), name='profile-detail')
]
