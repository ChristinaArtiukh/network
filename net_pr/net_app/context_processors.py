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


def list_for_qs(request, qs, list):
    for name, friend in qs:
        if name == request.user.id:
            list.append(friend)
        elif friend == request.user.id:
            list.append(name)
    return list


def list_for_all_friends(request):
    all_friends = []
    if request.user.is_authenticated:
        friends = Friends.objects.values_list('name', 'friend').filter(Q(name=request.user) | Q(friend=request.user))
        all_friends = list_for_qs(request, friends, all_friends)
    return all_friends


def list_for_approve(request):
    approve_friends = []
    if request.user.is_authenticated:
        approve = Friends.objects.values_list('name', 'friend').filter(approve_friendship=1)
        approve_friends = list_for_qs(request, approve, approve_friends)
    return approve_friends


def list_for_my_request(request):
    request_friends = []
    if request.user.is_authenticated:
        friends = Friends.objects.values_list('name', 'friend').filter(name=request.user, approve_friendship=0)
        request_friends = list_for_qs(request, friends, request_friends)
    return request_friends


def list_for_request_for_user(request):
    request_user_friends = []
    if request.user.is_authenticated:
        friends = Friends.objects.values_list('name', 'friend').filter(friend=request.user, approve_friendship=0)
        request_user_friends = list_for_qs(request, friends, request_user_friends)
    return request_user_friends


def is_valid_queryparam(param):
    return param != '' and param is not None


def searching(request):
    all_people = User.objects.filter(~Q(pk=request.user.id))
    search_request = request.GET.get('search')
    if is_valid_queryparam(search_request):
        search_list = search_request.split()
        for search in search_list:
            all_people = all_people.filter(Q(last_name__icontains=search)
                                           | Q(first_name__icontains=search)
                                           | Q(username__icontains=search))
    return all_people


def view_for_all_user(request):
    all_friend = list_for_all_friends(request)
    approve_friends = list_for_approve(request)
    request_friends = list_for_my_request(request)
    request_user_friends = list_for_request_for_user(request)
    other_people = User.objects.filter(~Q(pk=request.user.id)).filter(~Q(pk__in=all_friend))
    all_people = searching(request)
    context = {
        'other_people': other_people,
        'all_people': all_people,
        'all_friend': all_friend,
        'approve_friends': approve_friends,
        'request_friends': request_friends,
        'request_user_friends': request_user_friends,
        }
    return context


