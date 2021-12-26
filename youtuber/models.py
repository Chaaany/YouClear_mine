from django.db import models
from django.db.models.deletion import CASCADE
from taggit.managers import TaggableManager
from accounts.models import User

# Create your models here.

class Youtuber(models.Model):
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    name = models.CharField(max_length=100, unique=True)
    channel_id = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=30, blank=True)
    tag = TaggableManager(blank=True)
    detail_description = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'youtuber'
    
    def __str__(self):
        return self.name
 
# 유투버 별 비디오
class Video(models.Model):
    youtuber_name = models.ForeignKey(Youtuber, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=100)
    video_url = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-upload_date', '-update_date']
        verbose_name = 'video'
    def __str__(self):
        return self.video_name
    
# 마이 유투버 
class MyYoutuber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtuber = models.ForeignKey(Youtuber, on_delete=models.CASCADE, blank=True)
    listed_date = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.user} | {self.youtuber}'

    class meta:
        ordering = ['-listed_date']
        verbose_name = 'myyoutuber'

# 유투버 리스트, 마이 유투버 리스트
class YoutuberList(models.Model):
    main_title = models.CharField(max_length=40)
    sub_title = models.CharField(max_length=40)
    youtubers = models.ManyToManyField(Youtuber, related_name="youtuber_list")
    list_activated = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tag = TaggableManager(blank=True)

    def __str__(self):
        return f'{self.sub_title} {self.main_title}'
    
    class meta:
        ordering = ['-create_date', 'update_date']
    
class MyYoutuberList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtuber_list = models.ForeignKey(YoutuberList, on_delete=models.CASCADE, blank=True)
    listed_date = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.user} | {self.youtuber_list}'

    class meta:
        ordering = ['-listed_date']
        verbose_name = 'my_youtuber_list'