from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from googleapiclient.discovery import build
from .models import Video

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

    return search_response


def search(request):
    context = {}
    keyword = request.GET.get('keyword')
    page_token = request.GET.get('page_token')
    if keyword:
        response = youtube_search(keyword, page_token)
        context['keyword'] = keyword
        context['response'] = response
    return render(request, 'video/search.html', context)


def add_bookmark(request):
    if request.method == "POST":
        kind = request.POST.get('kind')
        youtube_id = request.POST.get('youtube_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        published_date = request.POST.get('published_date')
        thumbnail = request.POST.get('thumbnail')
        print(kind, youtube_id, title, description, published_date, thumbnail)
        # Video.objects.create(
        #     kind=kind,
        #     youtube_id=youtube_id,
        #     title=title,
        #     description=description,
        #     published_date=published_date,
        #     thumbnail=thumbnail,
        # )

        return HttpResponseRedirect('bookmark_list')
    else:
        return HttpResponse("nope")


def bookmark_list(request):
    bookmark_lists = Video.objects.all()
    context = {
        'bookmark_lists': bookmark_lists,
    }
    return render(request, 'video/bookmark_list.html', context)
