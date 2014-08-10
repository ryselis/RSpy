from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^index$', 'ge_api.views.index'),
    url(r'^ge/highalch$', 'ge_api.views.highalch')
)