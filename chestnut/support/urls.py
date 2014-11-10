from django.conf.urls import include, patterns, url

urlpatterns = patterns('',
                       url(r'^wechat/', include('chestnut.support.wechat.urls', namespace='chestnut.support.wechat'))
                       )
