from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^login$', 'chestnut.account.views.login', name='login'),
    url(r'^logout$', 'chestnut.account.views.logout', name='logout'),
    url(r'^signup$', 'chestnut.account.views.signup', name='signup'),
]
