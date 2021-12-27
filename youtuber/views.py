from django import contrib
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Youtuber, YoutuberList, MyYoutuberList, MyYoutuber, Video
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import User
from django.contrib import messages
from YouClear.settings import MEDIA_ROOT, MEDIA_URL
from taggit.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
# 유투브 api 사용
from .youtube_api import get_video_id_by_url, get_video_info, get_url_to_image, get_channel_info

def index(request):
    # 최신순으로 정렬(유투버 5명 / 유투버리스트 3개)
    youtubers = Youtuber.objects.all().order_by('-create_date')[0:10]
    youtuber_lists = YoutuberList.objects.all().order_by('-create_date')
    my_youtuber_lists = MyYoutuberList.objects.filter(user=request.user.id, activated=True)
    check_my_youtuber_lists = [my_list.youtuber_list for my_list in my_youtuber_lists]

    context = {
        'youtubers': youtubers, 
        'youtuber_lists': youtuber_lists,
        'check_my_youtuber_lists': check_my_youtuber_lists,
    }
    
    return render(request, 'youtuber/index.html', context)

@login_required
def youtuber(request, youtuber_id):
    try: 
        my_youtuber = MyYoutuber.objects.get(user=request.user.id, youtuber=youtuber_id, activated=True)
    except ObjectDoesNotExist:
        my_youtuber = None

    try:
        youtuber = Youtuber.objects.get(pk=youtuber_id)
        videos = Video.objects.filter(youtuber_name=youtuber_id)
        context = {'youtuber': youtuber, 'videos': videos}
    except Youtuber.DoesNotExist:
        raise Http404('유투버명을 확인해 주세요!')

    context['my_youtuber'] = my_youtuber is None

    return render(request, 'youtuber/youtuber.html', context)

@login_required
def edit_youtuber(request, youtuber_id):
    if request.user.is_superuser:
        try:
            youtuber = Youtuber.objects.get(id=youtuber_id)
        except ObjectDoesNotExist:
            return redirect('youtuber:index')
        # get 호출일 경우 수정 페이지 호출
        if request.method == 'GET':
            context = {'youtuber': youtuber}
            return render(request, 'youtuber/edit_youtuber.html', context)
        
        # Post 호출일 경우 수정 
        elif request.method == 'POST':
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                youtuber.profile_image = profile_image
                
            youtuber.name = request.POST.get('youtuber_name')
            youtuber.channel_id = request.POST.get('channel_id')
            youtuber.description =request.POST.get('youtuber_dsc')
            youtuber.detail_description = request.POST.get('detail_description')
            
            youtuber.save()

            return redirect('youtuber:youtuber', youtuber_id=youtuber.id)
    else:
        return redirect('youtuber:youtuber', youtuber_id=youtuber_id)

@login_required
def delete_youtuber(request, youtuber_id):
    if request.user.is_superuser:
        try:
            youtuber = Youtuber.objects.get(id=youtuber_id)
        except ObjectDoesNotExist:
            return redirect('youtuber:youtuber', youtuber_id=youtuber_id)
        
        youtuber.delete()

        return redirect('youtuber:index')
    
    else:
        return redirect('youtuber:youtuber', youtuber_id=youtuber_id)

        
@login_required
def my_youtuber(request, user_id):
    if user_id == request.user.id:
        my_youtubers = MyYoutuber.objects.filter(user=user_id, activated=True).order_by('-listed_date')
        context = {'my_youtubers': my_youtubers}
        
        return render(request, 'youtuber/my_youtuber.html', context)
    
    return redirect('youtuber:index')

@login_required
def add_my_youtuber(request, youtuber_id):

    my_youtuber, created = MyYoutuber.objects.get_or_create(
        user= User.objects.get(pk=request.user.id),
        youtuber= Youtuber.objects.get(pk=youtuber_id),
    )
    if not created:
        my_youtuber.activated = True
        my_youtuber.listed_date = timezone.now()
        my_youtuber.save()

    return redirect('youtuber:youtuber', youtuber_id)

@login_required
def remove_my_youtuber(request, youtuber_id):
    my_youtuber = MyYoutuber.objects.get(user=request.user.id, youtuber=youtuber_id)
    my_youtuber.activated = False
    my_youtuber.save()

    return redirect('youtuber:youtuber', youtuber_id)

@login_required
def delete_my_youtuber(request, youtuber_id):
    my_youtuber = MyYoutuber.objects.get(user=request.user.id, youtuber=youtuber_id)
    my_youtuber.activated = False
    my_youtuber.save()

    return redirect('youtuber:edit_my_youtuber', request.user.id)

@login_required
def edit_my_youtuber(request, user_id):
    my_youtubers = MyYoutuber.objects.filter(user=user_id, activated=True).order_by('-listed_date')
    context = {'my_youtuber': my_youtubers}

    return render(request, 'youtuber/edit_my_youtuber.html', context)


# 유투버 리스트
@login_required
def my_youtuber_list(request, user_id):
    if user_id == request.user.id:
        my_youtuber_lists = MyYoutuberList.objects.filter(user=user_id, activated=True).order_by('-listed_date')
        context = {'my_youtuber_lists': my_youtuber_lists}
            
        return render(request, 'youtuber/my_youtuber_list.html', context)
    
    return redirect('youtuber:index')

@login_required
def add_my_youtuber_list(request, youtuber_list_id):
    my_youtuber_list, created = MyYoutuberList.objects.get_or_create(
        user= User.objects.get(pk=request.user.id),
        youtuber_list= YoutuberList.objects.get(pk=youtuber_list_id),
    )
    if not created:
        my_youtuber_list.activated = True
        my_youtuber_list.listed_date = timezone.now()
        my_youtuber_list.save()

    if "category" in request.META['HTTP_REFERER']:
        return redirect('youtuber:category')

    if "popular" in request.META['HTTP_REFERER']:
        return redirect('youtuber:popular_youtuber_list')

    return redirect('youtuber:index')


@login_required
def remove_my_youtuber_list(request, youtuber_list_id):
    my_youtuber_list = MyYoutuberList.objects.get(user=request.user.id, youtuber_list=youtuber_list_id)
    my_youtuber_list.activated = False
    my_youtuber_list.save()

    if "category" in request.META['HTTP_REFERER']:
        return redirect('youtuber:category')
    
    if "popular" in request.META['HTTP_REFERER']:
        return redirect('youtuber:popular_youtuber_list')

    return redirect('youtuber:index')


@login_required
def delete_my_youtuber_list(request, youtuber_list_id):
    my_youtuber_list = MyYoutuberList.objects.get(user=request.user.id, youtuber_list=youtuber_list_id)
    my_youtuber_list.activated = False
    my_youtuber_list.save()

    return redirect('youtuber:edit_my_youtuber_list', request.user.id)

@login_required
def edit_my_youtuber_list(request, user_id):
    my_youtuber_lists = MyYoutuberList.objects.filter(user=user_id, activated=True).order_by('-listed_date')
    context = {'my_youtuber_lists': my_youtuber_lists}

    return render(request, 'youtuber/edit_my_youtuber_list.html', context)


#  특정 유투버 영상 리스트
def _get_videos(youtuber_id):
    videos = Video.objects.filter(youtuber_name=youtuber_id)
    videos = [video for video in videos]
    return videos

@login_required
# 마이리스트 상세페이지
def youtuber_list_detail(request,youtuber_list_id, youtuber_id=None):
    youtuber_list = YoutuberList.objects.get(id=youtuber_list_id)
    youtubers = youtuber_list.youtubers.all()
    videos = []
    
    if youtuber_id == None:
        for youtuber in youtubers:
            videos += _get_videos(youtuber.id)
            # print(videos)
        context = {
            'youtuber_list_id': youtuber_list_id,
            'youtuber_list': youtuber_list,
            'youtubers': youtubers,
            'videos': videos
        }
        return render(request, 'youtuber/youtuber_list_detail.html', context)
    else:
        videos = _get_videos(youtuber_id)
        # print(videos)
        context = {
            'youtuber_list_id': youtuber_list_id,
            'youtuber_id': youtuber_id,
            'youtuber_list': youtuber_list,
            'youtubers': youtubers,
            'videos': videos
        }
        return render(request, 'youtuber/youtuber_list_detail_specific_youtuber.html', context)

@login_required
def category(request, tag_slug=None):
    youtubers = Youtuber.objects.all()
    youtuber_lists = YoutuberList.objects.all().order_by('-create_date')
    all_tags = list(Tag.objects.all().filter(taggit_taggeditem_items__content_type__id=13))
    my_youtuber_lists = MyYoutuberList.objects.filter(user=request.user.id, activated=True)
    check_my_youtuber_lists = [my_list.youtuber_list for my_list in my_youtuber_lists]
# 필터 적용 전 전체 리스트 나열
    if tag_slug == None:
        context = {
            'youtubers': youtubers, 
            'youtuber_lists': youtuber_lists,
            'check_my_youtuber_lists': check_my_youtuber_lists,
            'all_tags': all_tags,
        }
        return render(request, 'youtuber/category.html', context)

# 특정 태그로 필터 후 리스트 나열
    else:
        specific_youtuber_lists = YoutuberList.objects.filter(tag__slug__in=[tag_slug])
        # print(specific_youtuber_lists)
        context = {
            'youtubers': youtubers, 
            'youtuber_lists': youtuber_lists,
            'specific_youtuber_lists': specific_youtuber_lists,
            'check_my_youtuber_lists': check_my_youtuber_lists,
            'all_tags': all_tags,
            'specific_tag_slug': tag_slug
        }
        
        return render(request, 'youtuber/category_specific.html', context)

@login_required
def admin_only(request):
    if request.user.is_superuser:
        return render(request, 'youtuber/admin_only.html')
    else:
        redirect('youtuber:index')

@login_required
# 관리자 계정일 경우 유투버(채널) 등록
def register_youtuber(request):
    if request.method == 'POST':
        if not request.POST.get('channel_id'):
            messages.info(request, '유투버(채널) id를 넣어주세요')
            return redirect('youtuber:admin_only')
        if not request.POST.get('youtube_api_key'):
            messages.info(request, 'api key를 넣어주세요')
            return redirect('youtuber:admin_only')
        channel_id = request.POST.get('channel_id')
        youtube_api_key = request.POST.get('youtube_api_key')
        
        channel_info = get_channel_info(developer_api_key = youtube_api_key, channel_Id = channel_id)
        
        if type(channel_info) is dict:
            # 썸네일 url to jpg 파일 처리
            channel_thumbsnail_url = get_url_to_image(
                thumbsnail_url = channel_info['channelThumbnailUrl'], 
                out_path = f'{MEDIA_ROOT}/profile/', # 개발서버 media 파일에 저장하기 위한 패스
                channel_title = channel_info['channelTitle'],
            )
            # 유투버(채널) 없을 시 objects 생성, 있을 시 get
            youtuber, created = Youtuber.objects.get_or_create(
                
                name = channel_info['channelTitle'],
                channel_id = channel_info['channelId'],
                detail_description = channel_info['channelDescription'],
                profile_image = '/profile/' + channel_info['channelTitle'] + '.jpg'
            )
            # get_or_create의 두 번째 return 값이 Boolean 값임 새로 생성 시 True 
            if created:
                messages.info(request, f'유투버(채널) 등록이 완료 되었습니다. 유투버(채널)명은 {youtuber}입니다.')
                return redirect('youtuber:admin_only')
            else:
                messages.info(request, f'해당 영상은 이미 등록되어 있습니다.\n"{youtuber}"입니다.')
                return redirect('youtuber:admin_only')
        else:
            messages.info(request, f'{channel_info}')
            return redirect('youtuber:admin_only')
    return redirect('youtuber:admin_only')

@login_required
# 관리자 계정일 경우 video 등록
def register_video(request):
    if request.method == 'POST':
        if not request.POST.get('video_id'):
            messages.info(request, '비디오 id를 넣어주세요')
            return redirect('youtuber:admin_only')
        if not request.POST.get('youtube_api_key'):
            messages.info(request, 'api key를 넣어주세요')
            return redirect('youtuber:admin_only')

        video_id = request.POST.get('video_id')
        youtube_api_key = request.POST.get('youtube_api_key')
        
        if 'http' in video_id  or 'youtube' in video_id:
            video_id = get_video_id_by_url(video_id)
            print(video_id)
            video_info = get_video_info(developer_api_key = youtube_api_key, videoId = video_id)
        else:
            video_info = get_video_info(youtube_api_key ,video_id)
        
        if type(video_info) is dict:
            try:
                youtuber = Youtuber.objects.get(name=video_info['channelTitle'])
            except ObjectDoesNotExist:
                messages.info(request, f"유투버(채널)부터 등록해 주세요.\n\"{video_info['channelTitle']}\"의 [{video_info['videoTitle']}]")
                return redirect('youtuber:admin_only')

            video, created = Video.objects.get_or_create(
                youtuber_name = youtuber,
                video_name = video_info['videoTitle'],
                video_url = video_info['VideoId']
            )
            if created:
                messages.info(request, f'영상 등록이 완료 되었습니다. \n"{youtuber.name}"의 [{video.video_name}]입니다')
                return redirect('youtuber:admin_only')
            else:
                messages.info(request, f'해당 영상은 이미 등록되어 있습니다.\n"{youtuber.name}"의 [{video.video_name}]입니다.')
                return redirect('youtuber:admin_only')
        else:
            messages.info(request, f'{video_info}')

    return redirect('youtuber:admin_only')

@login_required
def popular_youtuber_list(request):
    my_youtuber_lists = MyYoutuberList.objects.filter(user=request.user.id, activated=True)
    check_my_youtuber_lists = [my_list.youtuber_list for my_list in my_youtuber_lists]

    youtuber_lists = YoutuberList.objects.annotate(num_user=Count('myyoutuberlist')).order_by('-num_user', 'create_date')
    youtuber_lists = youtuber_lists.filter(myyoutuberlist__activated=True)[0:10]
    
    count_list = [list.myyoutuberlist_set.filter(activated=True).count() for list in youtuber_lists]

    context = {
        'youtuber_lists': youtuber_lists,
        'check_my_youtuber_lists': check_my_youtuber_lists,
        'count_list':count_list
        }
    for list in youtuber_lists:
        print(list, list.myyoutuberlist_set.filter(activated=True).count())
    return render(request, 'youtuber/popular_list.html', context)

def maps(request):
  return render(request, 'youtuber/map.html')