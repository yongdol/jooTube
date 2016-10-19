from django.http import HttpResponse
from googleapiclient.discovery import build

from video.models import Video

DEVELOPER_KEY = "AIzaSyDqBzZV0nqWGKd7oGMR7e6ZsQ1KdWUA-dk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(keyword, page_token, max_results=10):
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(
        q=keyword,
        part="id,snippet",
        maxResults=max_results,
        pageToken=page_token,
        ).execute()

    video_id_list = []
    for item in search_response['items']:
        id_kind = item['id']['kind'][8:]
        # print(id_kind)
        if id_kind == "video":
            video_id = item['id']['videoId']
        elif id_kind == "channel":
            video_id = item['id']['channelId']
        elif id_kind == "playlist":
            video_id = item['id']['playlistId']
        else:
            print("%s"%id_kind)
        video_id_list.append(video_id)

    # for video_id in video_id_list:
    #     if Video.objects.filter(youtube_id=video_id).exists():
    #         item['is_exist'] = True
    #     else:
    #         item['is_exist'] = False

    str_video_id_list = ','.join(video_id_list)
    # print("str : %s"%str_video_id_list)

    video_response = youtube.videos().list(
        part="id,snippet,statistics,contentDetails",
        id=str_video_id_list,
        maxResults=max_results,
        ).execute()

    """
    video_response 에는 pagetoken 값이 없어서 pagenation 이 불가.
    search_response 의 pagetoken 값을 video_response dict 에 추가.
    totalResult 값도 같은이유로 추가.
    """
    try:
        video_response['nextPageToken'] = search_response['nextPageToken']
    except:
        pass

    try:
        video_response['prevPageToken'] = search_response['prevPageToken']
    except:
        pass

    video_response['totalResults'] = search_response['pageInfo']['totalResults']

    for video_id in video_id_list:
        # print(Video.objects.filter(youtube_id=video_id))
        if Video.objects.filter(youtube_id=video_id).exists():
            video_response['is_exist'] = True
        else:
            video_response['is_exist'] = False
    return video_response

