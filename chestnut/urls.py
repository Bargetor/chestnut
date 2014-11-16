from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

from chestnut.support.wechat import views

urlpatterns = [
    # Examples:
    url(r'^$', 'chestnut.views.index', name='index'),

    #api
    url(r'^api/', include('bargetor.api.urls', namespace= 'api')),
    url(r'^api$', include('bargetor.api.urls', namespace= 'api')),

    #admin
    url(r'^admin/', include(admin.site.urls)),

    #support
    url(r'^chestnut/support/', include('chestnut.support.urls', namespace= 'chestnut.support')),

    #account
    url(r'^account/', include('chestnut.account.urls', namespace = 'account')),
    # url(r'^chestnut/support/wechat/user_info/$', views.user_info)
]
