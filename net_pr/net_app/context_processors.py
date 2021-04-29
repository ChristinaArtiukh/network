from django.db.models import Count, Q
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.template import Context

from .models import Friend, User


def vertical_nav(request, add_friends_count=None):
    if request.user.is_authenticated:
        add_friends_count = Friend.objects.filter(friend=request.user, approve_friendship=False).annotate(
            count=Count('approve_friendship')).values_list('count', flat=True)
    context = {
        'add_friends_count': add_friends_count,
    }
    return context


def searching(request):
    qs = User.objects.all().order_by('-date_join')
    search = request.GET.get('search')
    if search != '' and search is not None:
        qs = qs.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
    context = {
        'qs': qs,
        }

    print('context',  context)
    return context

