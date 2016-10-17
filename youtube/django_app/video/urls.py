from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'search/$', views.search, name='search'),
    url(r'add_bookmark', views.add_bookmark, name='add_bookmark'),
    url(r'bookmark_list', views.bookmark_list, name='bookmark_list'),
]