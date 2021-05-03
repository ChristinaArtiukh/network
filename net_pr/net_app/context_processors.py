from django.db.models import Count, Q
from .models import Friends, User


def vertical_nav(request, add_friends_count=None):
    if request.user.is_authenticated:
        add_friends_count = Friends.objects.filter(friend=request.user, approve_friendship=False).annotate(
            count=Count('approve_friendship')).values_list('count', flat=True)
    context = {
        'add_friends_count': add_friends_count,
    }
    return context


def all_friends(request):
    all_friends = []
    if request.user.is_authenticated:
        friends = Friends.objects.values_list('name', 'friend').filter(Q(name=request.user) | Q(friend=request.user))
        for name, friend in friends:
            if name == request.user.id:
                all_friends.append(friend)
            elif friend == request.user.id:
                all_friends.append(name)
    return all_friends


def approve(request):
    approve_friends = []
    if request.user.is_authenticated:
        approve = Friends.objects.values_list('name', 'friend').filter(approve_friendship=1)
        for name, friend in approve:
            if name == request.user.id:
                approve_friends.append(friend)
            elif friend == request.user.id:
                approve_friends.append(name)
        return approve_friends


def my_request(request):
    request_friends = []
    if request.user.is_authenticated:
        friends = Friends.objects.values_list('name', 'friend').filter(name=request.user, approve_friendship=0)
        for name, friend in friends:
            if name == request.user.id:
                request_friends.append(friend)
            elif friend == request.user.id:
                request_friends.append(name)
    return request_friends


def request_for_user(request):
    request_user_friends = []
    if request.user.is_authenticated:
        friends = Friends.objects.values_list('name', 'friend').filter(friend=request.user, approve_friendship=0)
        for name, friend in friends:
            if name == request.user.id:
                request_user_friends.append(friend)
            elif friend == request.user.id:
                request_user_friends.append(name)
    return request_user_friends


def is_valid_queryparam(param):
    return param != '' and param is not None


def view_for_all_user(request):
    all_friend = all_friends(request)
    approve_friends = approve(request)
    request_friends = my_request(request)
    request_user_friends = request_for_user(request)
    friends = Friends.objects.all().filter(Q(name=request.user) | Q(friend=request.user))
    other_people = User.objects.filter(~Q(pk=request.user.id)).filter(~Q(pk__in=all_friend))
    all_people = User.objects.filter(~Q(pk=request.user.id))
    search = request.GET.get('search')
    if is_valid_queryparam(search):
        search_list = search.split()
        for i in search_list:
            all_people = all_people.filter(Q(last_name__icontains=i)
                                           | Q(first_name__icontains=i)
                                           | Q(username__icontains=i))
    context = {
        'other_people': other_people,
        'all_people': all_people,
        'all_friend': all_friend,
        'approve_friends': approve_friends,
        'request_friends': request_friends,
        'request_user_friends': request_user_friends,
        'friends': friends,
        }
    return context

