from django.conf.urls import patterns,include,url
from . import views

urlpatterns=patterns('',
                     url(r'^$',views.home_page,name='home'),
                     url(r'^about/$',views.aboutpage,name='about'),
                     url(r'^login/$',views.login_user,name='login'),
                     url(r'^logout/$',views.logout_user,name='logout'),
                     url(r'^registration/$',views.registrate,name='reg'),
                     url(r'^mypage/edit/$',views.profileedit,name='edit'),
                     url(r'^mypage/view/$',views.profileview,name='view'),
                     url(r'^mypage/mybookings/$',views.myBookings,name='mybookings'),
                     url(r'^mypage/myservices/$',views.myServices,name='myservices'),
                     url(r'^mypage/staff/corpbooking/(?P<sdate>[-0-9:]+)/(?P<edate>[-0-9:]+)/(?P<cob>[0-9]+)/$',views.companylist,name='complist'),
                     url(r'^mypage/staff/income/(?P<sdate>[-0-9:]+)/(?P<edate>[-0-9:]+)/$',views.income,name='income'),
                     url(r'^mypage/staff/newusers/(?P<sdate>[-0-9:]+)/(?P<edate>[-0-9:]+)/$',views.newusers,name='newusers'),
                     url(r'^mypage/staff/newusers/detail/(?P<user_id>[0-9]+)/$',views.userdetail,name='userdetail'),
                     url(r'^mypage/addmoney/$',views.addmoney,name='addmoney'),
                     url(r'^mypage/staff/corpbooking/(?P<sdate>[-0-9:]+)/(?P<edate>[-0-9:]+)/(?P<comp_id>[0-9]+)/detail/$',views.compdetail,name='compdetail'),
                     url(r'^mypage/discounts/list/(?P<sdate>[-0-9:]+)/$',views.discountlist,name='discslist'),
                     url(r'^mypage/discounts/detail/(?P<disc_id>[-0-9:]+)/$',views.discountdetail,name='discdetail'),

                     )
