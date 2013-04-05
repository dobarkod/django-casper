from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'testapp.views.index', name='index')  # flake8: noqa
)
