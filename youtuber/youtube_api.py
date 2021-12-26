from googleapiclient.discovery import build
import urllib.parse as p
import urllib.request
import os
from tkinter import messagebox

# url 넣으면 videoid만 추출해 주는 메소드
def get_video_id_by_url(url):
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")

# video 데이터 입력용 메소드 api key와 video Id 넣으면 data return
def get_video_info(developer_api_key, videoId):
    # youtube api 사용하기 위한 기본 정보 (디벨로퍼 키 반드시 파라미터로 넣기)
    developer_key = developer_api_key
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION, 
        developerKey=developer_key 
    )
    # youtube videos.list api 호출
    try:
        video = youtube.videos().list(
            part = "id, snippet",
            id = videoId,
        ).execute()
    except:
        return 'api key 값을 확인해 주세요'

    # video resource 호출
    try:
        video_item = video['items'][0]
    except:
        return '해당하는 영상이 없습니다.'

    # video 등록에 필요한 정보만 추출
    video_content = {
        "channelId": video_item['snippet']['channelId'], # video의 channel id
        "channelTitle": video_item['snippet']['channelTitle'], # video의 channel name
        "videoTitle": video_item['snippet']['title'], # video의 title
        "VideoId": video_item['id'], # video의 id
    }

    return video_content


# 웹 url을 png파일로 변환
def get_url_to_image(thumbsnail_url, out_path, channel_title):
#저장할 웹 이미지 주소
    outpath = out_path #지정 이미지 저장 폴이

    if not os.path.isdir(outpath): #폴더가 존재하지 않는다면 폴더 생성
        os.makedirs(outpath)

    outfile = channel_title + ".jpg"
    urllib.request.urlretrieve(thumbsnail_url, outpath+outfile)

    thumbsnail_url_path = outpath+outfile

    return thumbsnail_url_path

# youtuber 등록시 필요한 channel_info
def get_channel_info(developer_api_key, channel_Id):
    developer_key = developer_api_key
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION, 
        developerKey=developer_key 
    )
    # youtube videos.list api 호출
    try:
        channel = youtube.channels().list(
        part = "id, snippet",
        id = channel_Id,
        ).execute()
    except:
        return 'api key 값을 확인해 주세요'

    try:
        channel_items = channel['items'][0]
    except:
        return '해당하는 유투버(채널)이 없습니다.'

    channel_content = {
        'channelId': channel_Id,
        'channelTitle': channel_items['snippet']['title'],
        'channelThumbnailUrl': channel_items['snippet']['thumbnails']['default']['url'],
        'channelDescription': channel_items['snippet']['description']
    }

    return channel_content

# video id 넣었을 때 유투버 없으면 유투버까지 넣어주려고 하려고 만들었으나 아직 미완
def _get_playlist_info(developer_api_key, playlist_Id):
    developer_key = developer_api_key
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION, 
        developerKey=developer_key 
    )
    # youtube videos.list api 호출
    channel_Id = "UCWXoZbjwHKS4s0RyJCuoAQQ"

    video = youtube.playlistItems().list(
        part = "id, snippet",
        playlistId = "PL92z7eICcn9W5MRh47ax6529qC5SGV1m9",
        maxResults = 10
    ).execute()

    # video resource 호출
    print(video, "///////")

    video_item = video['items'][0]
    print(video_item)

