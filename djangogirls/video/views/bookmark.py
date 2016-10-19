from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from video.models import Video

__all__ = ['bookmark_list', 'bookmark_add', 'bookmark_detail', 'bookmark_delete']


def bookmark_add(request):
    path = request.POST.get('path')
    try:
        kind = request.POST['kind']
        youtube_id = request.POST['youtube_id']
        title = request.POST['title']
        description = request.POST['description']
        published_date = request.POST['published_date']
        thumbnail = request.POST['thumbnail']

        Video.objects.create(
            kind=kind,
            youtube_id=youtube_id,
            title=title,
            description=description,
            published_date=published_date,
            thumbnail=thumbnail,
        )
        msg = "success"
    except Exception as e:
        msg = 'nope %s'%e.args

    messages.success(request, msg)

    if path:
        return redirect(path)
    else:
        return redirect('video:bookmark_list')


def bookmark_list(request):
    videos = Video.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'video/bookmark_list.html', context)


def bookmark_detail(request, pk):
    video = Video.objects.get(pk=pk)
    # print(video.youtube_id)
    context = {
        'video': video,
    }
    return render(request, 'video/bookmark_detail.html', context)


def bookmark_delete(request, pk):
    video = Video.objects.get(pk=pk)
    video.delete()
    return redirect('video:bookmark_list')


