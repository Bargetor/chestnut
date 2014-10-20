from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'chestnut.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('api.urls', namespace= 'api')),
    url(r'^api$', include('api.urls', namespace= 'api')),
    url(r'^admin/', include(admin.site.urls)),
]
