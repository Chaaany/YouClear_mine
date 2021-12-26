from django import template
from youtuber.models import *

register = template.Library()

@register.filter
def count_filter(value):
    count = MyYoutuberList.objects.filter(youtuber_list=value, activated=True).count()
    return count