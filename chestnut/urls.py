from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'chestnut.views.index', name='index'),
    url(r'^accounts/login$', 'chestnut.views.login', name='login'),
    url(r'^accounts/logout$', 'chestnut.views.logout', name='logout'),
    url(r'^accounts/signup$', 'chestnut.views.signup', name='signup'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('api.urls', namespace= 'api')),
    url(r'^api$', include('api.urls', namespace= 'api')),
    url(r'^admin/', include(admin.site.urls)),
]
