from django.urls import path
from .views import *

app_name='youtuber'

urlpatterns = [
    path('', index, name='index'),    
    path('youtuber/<int:youtuber_id>/', youtuber, name='youtuber'),
    path('edit_youtuber/<int:youtuber_id>/', edit_youtuber, name='edit_youtuber'),
    path('delete_youtuber/<int:youtuber_id>/', delete_youtuber, name='delete_youtuber'),
    path('add/my_youtuber/<int:youtuber_id>/', add_my_youtuber, name='add_my_youtuber'), 
    path('remove/my_youtuber/<int:youtuber_id>/', remove_my_youtuber, name='remove_my_youtuber'),
    path('my_youtuber/<int:user_id>/', my_youtuber, name='my_youtuber'),
    path('edit_my_youtuber/<int:user_id>/', edit_my_youtuber, name='edit_my_youtuber'),
    path('delete_my_youtuber/<int:youtuber_id>/', delete_my_youtuber, name='delete_my_youtuber'),
    path('my_youtuber_list/<int:user_id>/', my_youtuber_list, name='my_youtuber_list'),
    path('add/my_youtuber_list/<int:youtuber_list_id>/', add_my_youtuber_list, name='add_my_youtuber_list'), 
    path('remove/my_youtuber_list/<int:youtuber_list_id>/', remove_my_youtuber_list, name='remove_my_youtuber_list'),
    path('edit_my_youtuber_list/<int:user_id>/', edit_my_youtuber_list, name='edit_my_youtuber_list'),
    path('delete_my_youtuber_list/<int:youtuber_list_id>/', delete_my_youtuber_list, name='delete_my_youtuber_list'),
    path('youtuber_list_detail/<int:youtuber_list_id>/', youtuber_list_detail, name='youtuber_list_detail'),
    path('youtuber_list_detail/<int:youtuber_list_id>/<int:youtuber_id>', youtuber_list_detail, name='youtuber_list_detail_specific_youtuber'),
    path('category/', category, name='category'),
    path('category/<slug:tag_slug>/', category, name='category_specific'),
    path('admin_only/', admin_only, name='admin_only'),
    path('admin_only/register_youtuber/', register_youtuber, name='register_youtuber'),
    path('admin_only/register_video/', register_video, name='register_video'),
    path('youtuber_list/popular/', popular_youtuber_list, name='popular_youtuber_list'),
]