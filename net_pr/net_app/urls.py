from django.urls import path
from .views import home, registration, user_logout, add_profile, profile, FriendsListView

urlpatterns = [
    path('', home, name='home'),
    path('login_registration/', registration, name='registration'),
    path('logout/', user_logout, name='logout'),
    path('profile/add', add_profile, name='add_profile'),
    path('profile/<slug:slug>', profile, name='profile'),
    path('friends/', FriendsListView.as_view(), name='friends')


]