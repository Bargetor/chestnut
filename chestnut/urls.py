from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'chestnut.views.index', name='index'),
    url(r'^login$', 'chestnut.views.login', name='login'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('api.urls', namespace= 'api')),
    url(r'^api$', include('api.urls', namespace= 'api')),
    url(r'^admin/', include(admin.site.urls)),
]
