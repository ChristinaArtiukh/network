from django.urls import path
from .views import home, registration, user_logout, add_profile, profile, UpdateUserInfo,\
    users_list, friends_list

urlpatterns = [
    path('', home, name='home'),
    path('login_registration/', registration, name='registration'),
    path('logout/', user_logout, name='logout'),
    path('profile/<slug:slug>/add', add_profile, name='add_profile'),
    path('profile/<slug:slug>', profile, name='profile'),
    path('all/', users_list, name='all'),
    path('profile/<slug:slug>/update', UpdateUserInfo.as_view(), name='update_profile'),
    path('friends/', friends_list, name='friends'),

]