from django.conf.urls import patterns, url
from chestnut.support.wechat import views

urlpatterns = patterns('',
                       url(r'^user_info/$', views.user_info, name = 'user_info')
                       )
