from django.db.models import Count
from .models import Friend


def vertical_nav(request, add_friends_count=None):
    if request.user.is_authenticated:
        add_friends_count = Friend.objects.filter(friend=request.user, approve_friendship=False).annotate(
            count=Count('approve_friendship')).values_list('count', flat=True)

    context = {
        'add_friends_count': add_friends_count,
    }

    return context