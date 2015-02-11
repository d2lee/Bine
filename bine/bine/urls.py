from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from bine.views import BookList, BookNoteList, BookNoteDetail,\
    BookNoteLikeItUpdate, BookNoteReplyDetail, BookNoteReplyList
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/static/bine/html/bine.html')),
    url(r'^book/$', BookList.as_view()),
    url(r'^note/$', BookNoteList.as_view()),
    url(r'^note/(?P<pk>[0-9]+)/$', BookNoteDetail.as_view()),
    url(r'^note/(?P<note_id>[0-9]+)/reply/$', BookNoteReplyList.as_view()),
    url(r'^note/(?P<note_id>[0-9]+)/reply/(?P<reply_id>[0-9]+)/$', BookNoteReplyDetail.as_view()),
    url(r'^note/(?P<note_id>[0-9]+)/likeit/', BookNoteLikeItUpdate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)