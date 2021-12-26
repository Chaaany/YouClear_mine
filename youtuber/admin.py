from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Youtuber)

admin.site.register(MyYoutuber)

admin.site.register(Video)

admin.site.register(YoutuberList)

admin.site.register(MyYoutuberList)
