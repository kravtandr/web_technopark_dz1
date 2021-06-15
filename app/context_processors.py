from .models import *

members = Profile.objects.best()[:5]
popular_tags = Tag.objects.popular()[:5]

def extras(request):
    return {
        'popular_tags':  Tag.objects.popular()[:5],
        'members': Profile.objects.best()[:5]
    }