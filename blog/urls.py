from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^profile_list$', views.researcher_profile_list),
    url(r'^profile/search$', views.search),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.researcher_detail),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),    
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),    
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),    
    url(r'^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),    
    #url(r'^accounts/register/$', views.register, name="register"),    
    
    #System automatically redirect the request to login to url "accounts/login" 
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),    
    #For cayley 
    url(r'^cayley/response/$', views.cayley_show_all_vertex),    
    url(r'^cayley/(?P<tmpID>[0-9]+)/$', views.cayley_detail),
    url(r'^test/$', views.test),
    url(r'^searchStaticFiles/$', views.searchStaticFiles),
    
    url('^', include('django.contrib.auth.urls')),
]
