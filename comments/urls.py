from django.conf.urls import patterns,include,url
from . import views

urlpatterns=patterns('',
                     url(r'^$',views.CommentView,name='view'),
                     url(r'^detail/(?P<comment_id>[0-9]+)/$',views.detail,name='detail'),
                     url(r'^detail/(?P<comment_id>[0-9]+)/like/$',views.like,name='like'),
                     url(r'^edit/$', views.CreateCommentView.as_view(success_url="/comments/"),name='edit'),
                     )
