from django.conf.urls import patterns,include,url
from bill.views import *

urlpatterns=patterns('',
                     url(r'^$',BookingView.as_view(success_url="/mypage/mybookings/"),name='booking'),
                     url(r'^conf/(?P<booking_id>[-0-9]+)/$',ConfirmtheBookingView,name='conf'),
                     url(r'^conf/(?P<booking_id>[-0-9]+)/valid/$',ValidBooking,name='valid'),
                     url(r'^conf/(?P<booking_id>[-0-9]+)/delete/$',DeleteBooking,name='delete'),
                     url(r'^room/(?P<sdate>[-0-9]+)/(?P<edate>[-0-9]+)/$',FindFreeRoom,name='freeroom'),
                     url(r'^room/(?P<sdate>[-0-9]+)/(?P<edate>[-0-9]+)/(?P<style>[a-z]+)/$',FindFreeRoomWS,name='freeroomws'),
                     url(r'^service/$',ServiceOrderView.as_view(success_url="/mypage/myservices/"),name='serviceorder'),
                     url(r'^service/list/$',servicelist,name='servicelist'),
                     url(r'^confservice/(?P<serviceorder_id>[-0-9]+)/$',ConfirmetheServiceOrderView,name='confservice'),
                     url(r'^confservice/(?P<serviceorder_id>[-0-9]+)/valid/$',ValidServiceOrder,name='validservice'),
                     url(r'^confservice/(?P<serviceorder_id>[-0-9]+)/delete/$',DeleteServiceOrder,name='deleteservice'),
                     url(r'^room/(?P<housing>[0-9]+)/(?P<floor>[0-9]+)/(?P<number>[0-9]+)/$',roomdetail,name='roomdetail'),
                     )
